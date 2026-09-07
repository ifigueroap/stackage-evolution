You are categorizing a Haskell source code from Stackage packages that features the Control.Monad.Reader import. 
Focus only on the usage of the Control.Monad.Reader. You will consider a use of Control.Monad.Reader everytime an api symbol listed on the synopsis appears in the code, without it being hidden at import or redefined. Also should consider use when the module is aliased or qualified.
You shall use only source-supported findings. Do not infer hidden types. You will be allowed to inspect other files from the package, only when its necessary for making an accurate categorization. You will be allowed to inspect up to 5 files so make sure that you inspect relevant files, and the ones that are most likely to clarify the uncertainty abaout the categorization.
This is the synopsis of Control.Monad.Reader:

class Monad m => MonadReader r (m :: Type -> Type) | m -> r where

    ask :: m r
    local :: (r -> r) -> m a -> m a
    reader :: (r -> a) -> m a

asks :: MonadReader r m => (r -> a) -> m a
type Reader r = ReaderT r Identity
runReader :: Reader r a -> r -> a
mapReader :: (a -> b) -> Reader r a -> Reader r b
withReader :: (r' -> r) -> Reader r a -> Reader r' a
newtype ReaderT r (m :: Type -> Type) a = ReaderT (r -> m a)
runReaderT :: ReaderT r m a -> r -> m a
mapReaderT :: (m a -> n b) -> ReaderT r m a -> ReaderT r n b
withReaderT :: forall r' r (m :: Type -> Type) a. (r' -> r) -> ReaderT r m a -> ReaderT r' m a
module Control.Monad.Trans


The first 4 lines you will receive are 4 lines are metadata (package, module, path)
and then goes the content of the file. 
The expected output is in Json style like this example:
{
"package_id": "equivalence-0.4.1.1",
"package": "equivalence",
"module": "Data.Equivalence.Monad",
"path": "src/Data/Equivalence/Monad.hs",
"comment": "defines a new monad transformer deriving MonadReader",
"explicit_import": false,
"api_usage": {
"MonadReader": 1,
"reader": 0,
"ask": 0,
"local": 0,
"asks": 0,
"Reader": 0,
"runReader": 0,
"withReader": 0,
"mapReader": 0,
"ReaderT": 1,
"runReaderT": 0,
"withReaderT": 0,
"mapReaderT": 0
},
"categories": {
"lifting_reader": true,
"lifting_readert": false,
"direct_use_pure": false,
"direct_use_inner": false,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": false,
"with_io": false,
"re_export": false
},
"need_review": true
}

Where, "package_id", "package", "module" "path" are given to you. 
"comment" Its an optional string with a brief comment about the module. Only use when explaining "need_review", noting unusual usage, suggesting new category and reporting ambiguous use cases or difficulty in finding a fitting category. If you inspect another file, it should be noted in the comment. Otherwise just "".
"explicit_import" this is a boolean, true if the functions of the module are imported explicitly using an import list (for example: import Control.Monad.Reader ( ReaderT )), false if not.
"need_review" is a boolean, true if you consider that no category fits properly, or if you lack context or information to properly categorize, or if simply there is something strange in the file. Leaving a brief comment about it in the "comment".
"api_usage" contains an int count for every class, type and function in the Control.Monad.Reader. Should only count the occurrences as they come from the import, for example, redefining "ask" in a nonrelated way no longer counts; although specifying ask in instancing for MonadReader or similar should be counted. Type signatures are counted as occurrences. Do not count the import or explicit import occurrences. A symbol is counted only when syntactically attributable to Control.Monad.Reader, either through its unqualified import binding or through a qualified/aliased import of Control.Monad.Reader
"categories" these are independent boolean properties, so a file might satisfy multiple categories simultaneously. "categories" contains the categories in which the usage of Control.Monad.Reader falls into for this file. A property or category is marked true if it fits the criteria for said category, which are explained later. Also mention that categories are not necessarily mutually exclusive and that a single file may contain several different uses, resulting in multiple categories being present.

There are 11 categories, and a file may present multiple categories (examples dont show the full file, only the Control.Monad.Reader related parts). Categories are not necessarily mutually exclusive; so a single file may contain several different uses, resulting in multiple categories being true simultaneously.
Here are the categories with examples:
1. lifting_reader: Mark lifting_reader = true when Reader-related capabilities are propagated through another monad transformer layer. This includes defining or using MonadReader instances that delegate Reader operations through another transformer, for example:

    instance MonadReader r m => MonadReader r (StateT s m) where
        ask = lift ask
        local f = mapStateT (local f)

The defining characteristic is that Reader/MonadReader behavior is explicitly lifted or propagated through a transformer layer other than ReaderT itself. Do not mark lifting_reader=true merely because ReaderT appears in an instance definition.

2. lifting_readert: Mark lifting_readert = true when ReaderT itself is being defined, instantiated, or given an instance that delegates another capability through the ReaderT layer. This includes:

    instance MonadReader r (ReaderT r m) where
        ask = ReaderT pure
        local f (ReaderT m) = ReaderT $ \r -> m (f r)

and instances such as:

    instance MonadWriter w m => MonadWriter w (ReaderT r m) where
        tell = lift . tell

    instance (Applicative m, Semigroup a) => Semigroup (ReaderT r m a) where
        (<>) = liftA2 (<>)

The defining characteristic is that ReaderT is itself the transformer layer whose instance or implementation is being defined.Do not mark direct_use_outer=true merely because such an instance exists. Mark direct_use_outer=true only when the file contains an actual concrete ReaderT computation used as the outer monad layer.
3. direct use (pure): Mark direct_use_pure=true when using Reader or ReaderT as the only monad layer with no transformer stack and no effects.
                      So (Reader w) (ReaderT w Identity) and aliases of them can be classified as pure.
4. direct use (inner): Reader or ReaderT is at the bottom of the stack, and there should be at least one layer wrapping it. So that the log persists through effects. The position is determined by the expanded transformer structure of the monad stack, not just by type synonyms. If a type alias obscures the stack, you may need to look at the actual definition.  
5. direct use (middle): Reader or ReaderT sits in the middle of a monad transformer stack, so there is at least a layer above and at least one below the reader.
6. direct use (outer):  Mark direct_use_outer when Reader or ReaderT is the outer layer (top of the stack) so the inner effects happen inside the Reader.
                        For example, (ReaderT w m a), where m has effects or is a transformer stack. But if just (Reader w a) then it is probably just direct_use_pure=true.
                        If ReaderT/runReaderT is used only to define a transformer instance that propagates reader-related behavior through the layer, classify it as lifting_readert=true. Do not mark direct_use_outer=true unless the file contains an actual concrete computation whose primary monad is ReaderT ... and not just an instance/lifted behavior definition.
7. polymorphic_use: Mark polymorphic_use = true when a function's implementation uses ask, local, reader, or asks (or any concrete Reader/ReaderT operations) within a polymorphic context where the concrete monad is specified only by a MonadReader constraint. The function must actually execute reader operations, not just mention them in type signatures. The actual monad is determined by the caller. This is distinct from constraint_only where the methods aren't actually used.
A type synonym or alias that expands to a concrete Reader/ReaderT stack does not constitute polymorphic use. For polymorphic_use=true, the function's monad must remain genuinely abstract through a type variable constrained by MonadReader (or equivalent polymorphic context). A function using asks, ask, local, reader, or similar operations in a concrete Reader/ReaderT type or a type synonym that expands to one is not polymorphic_use.
8. constraint_only: Mark constraint_only = true when the file references MonadReader (or any of its methods like ask, local, reader, asks) only in type signatures or class constraints, but executes no actual reader operations (no ask, local, reader, or asks calls), uses no concrete reader types (Reader, ReaderT, runReader, withReader, etc.), and defines no instances of MonadReader (that would be lifting). The reader appears solely as a constraint in type class definitions, function signatures, or data type contexts, serving as an API design element or future capability rather than being used for immediate functionality. This category is mutually exclusive with lifting_reader, lifting_readert, polymorphic_use, direct_use_inner,direct_use_middle, direct_use_outer and not_used.
9. not used:  mark not_used=true when the monad is not used, none of the functions defined by the Control.Monad.Reader are present. No use of class, type, constructor, function, method, or re-export. Also when the file only references reader as qualified Template Haskell quoted names in derive declarations for unrelated.
              Its expected that here the api_usage counts are 0.
10. with exeptions:  Mark with_exceptions=true when Reader a related computations is directly combined with an exception or error-handling abstraction such as ExceptT, MonadError, Either, ErrorT, throwError, catchError or similar abstractions; that are likely combined with Reader/ReaderT:
          ReaderT Config (ExceptT Error IO) a

          ExceptT Error (ReaderT Config IO) a

          foo :: MonadReader Config m => m (Either Error a)

          foo = do
              config <- ask
              ...

              -- with actual error-related handling

      Do not mark with_exceptions=true merely because:
      - an error-related module is imported.
      - an error type is declared or mentioned elsewhere.
      - an unrelated function uses Either.
      - a Reader-related function and an error-related function happen to occur in the same file without being directly combined.
      The category concerns the actual Reader-related usage, not merely the presence of error-related identifiers in the module. Simple cases of type declarations like "ReaderT Config IO (Either E A)" do count, even if no exception computation is performed.
11. with_IO:
true when the Reader/ReaderT computation is directly combined with IO
functionality in the same monad stack, or when an otherwise polymorphic
Reader stack is explicitly instantiated in the file with IO as its base
monad.

Examples:
  ReaderT Env IO a                              -> true
  ReaderT Env (StateT S IO) a                   -> true
  StateT S (ReaderT Env IO) a                   -> true
  ExceptT E (StateT S (ReaderT Env IO)) a       -> true
  Stack IO a                                    -> true
    if Stack is known to contain a Reader layer
  Reader Env a                                  -> false
  ReaderT Env Identity a                        -> false

An explicit IO specialization present in the file counts. For example, if:

  type Stack m a = StateT S (ReaderT Env m) a

then:

  foo :: Stack m a       -> does not establish with_IO
  foo :: Stack IO a      -> with_IO = true

The file does not need to call liftIO explicitly. The presence of IO in the
Reader-containing monad stack is sufficient.

Do not mark true merely because IO operations, MonadIO, or liftIO occur
elsewhere in the module. IO must be part of, or an explicit specialization
of, the Reader-containing computation being categorized.
12. with_writer:
true when the Reader/ReaderT computation is directly combined with
Writer/WriterT functionality in the same monad stack, or when an otherwise
polymorphic Reader stack is explicitly instantiated in the file with a
Writer/WriterT-based monad.

Examples:
  ReaderT Env (WriterT W IO) a                   -> true
  WriterT W (ReaderT Env IO) a                   -> true
  StateT S (ReaderT Env (WriterT W IO)) a        -> true
  Run (Writer W) a                               -> true
    if Run is known to contain a Reader layer
  Reader Env a                                   -> false

Do not mark true merely because Writer is imported or used in a separate,
unrelated computation.
13. with_state:
true when the Reader/ReaderT computation is directly combined with
State/StateT functionality in the same monad stack, or when an otherwise
polymorphic Reader stack is explicitly instantiated in the file with a
State/StateT-based monad.

Examples:
  ReaderT Env (StateT S IO) a                    -> true
  StateT S (ReaderT Env IO) a                    -> true
  ExceptT E (StateT S (ReaderT Env IO)) a        -> true
  Run (StateT S IO) a                            -> true
    if Run is known to contain a Reader layer
  Reader Env a                                   -> false

Do not mark true merely because State is imported or used in a separate,
unrelated computation.
14. with_parser:
true when the Reader/ReaderT computation is directly combined with a parser
monad or parser-transformer capability in the same computation or monad stack,
or when an otherwise polymorphic Reader stack is explicitly instantiated in
the file with a recognizable parser monad.

Examples:
  ReaderT Env (Parsec E S) a                     -> true
  StateT St (ReaderT Env (Parsec E S)) a         -> true
  ReaderT Env Parser a                           -> true
    if Parser is known to be a parser monad
  Run (Parsec E S) a                             -> true
    if Run is known to contain a Reader layer
  Reader Env a                                   -> false

Because parser monads are less standardized than StateT or WriterT, inspect
type aliases or newtype definitions when necessary to determine whether a
named monad is a parser monad.

Do not mark true merely because parsing functions or a parser library are used
elsewhere in the module.
15. Re-export: Mark re_export=true when any function or target symbol of Control.Monad.Reader are re-exported. Like, for example:
    -- Re-exporting the entire imported module:
    module Foo (module Control.Monad.Reader) where
    import Control.Monad.Reader
    -- Re-exporting individual imported symbols:
    module Foo (ask, ReaderT) where
    import Control.Monad.Reader (ask, ReaderT)
    --Re-exporting an imported qualified module alias:
    module Foo (module R) where
    import qualified Control.Monad.Reader as R

Explicit effect specialization rule:
For with_state, with_writer, with_parser, and with_IO, count explicit effect
specializations actually present in the file. If a Reader-containing stack is
normally polymorphic in a base monad m, but the file uses that stack with m
replaced by a recognizable effect monad, the corresponding with_* category is
true.

Examples:
  Stack m a                  -> no conclusion about the base effect
  Stack IO a                 -> with_IO = true
  Stack (Writer W) a         -> with_writer = true
  Stack (State S) a          -> with_state = true
  Stack (Parsec E S) a       -> with_parser = true

This rule applies only when Stack is known to contain a Reader/ReaderT layer.
--------  examples ---------
Here are examples and after all of them there is a list with the expected outputs. The (...) notes there is a chunk of code there, that has no presence of reader activity.
example 1:
    equivalence
    Data.Equivalence.Monad
    src/Data/Equivalence/Monad.hs

    newtype EquivT s c v m a = EquivT {unEquivT :: ReaderT (Equiv s c v) (STT s m) a}
        deriving (Functor, Applicative, Monad, MonadError e, MonadState st, MonadWriter w)

    instance (MonadEquiv c v d m, Monoid w) => MonadEquiv c v d (WriterT w m) where
        equate  x y = lift $ equate x y
        combine x y = lift $ combine x y
example 2: 
    servant-checked-exceptions-core
    Servant.Checked.Exceptions.Internal.EnvelopeT
    src/Servant/Checked/Exceptions/Internal/EnvelopeT.hs

    instance MonadWriter w m => MonadWriter w (EnvelopeT es m) where
        writer = lift . writer
        tell = lift . tell
        listen (EnvelopeT m) =
            EnvelopeT $ do
            (envelopeA, w) <- listen m
            pure $ fmap (,w) envelopeA
        pass (EnvelopeT m) =
            EnvelopeT $ do
            envel <- m
            pass . pure $
                case envel of
                SuccEnvelope (a, f) -> (SuccEnvelope a, f)
                ErrEnvelope es -> (ErrEnvelope es, id)
example 3:
    import Control.Monad.Writer.Strict
    interleaveRanges :: forall a. (HasRangeWithoutFile a) => [a] -> [a] -> ([a], [(a,a)])
    interleaveRanges as bs = runWriter $ go as bs
    where
        go []         as = return as
        go as         [] = return as
        go as@(a:as') bs@(b:bs') =
        let ra = getRangeWithoutFile a
            rb = getRangeWithoutFile b

            ra0 = rStart ra
            rb0 = rStart rb

            ra1 = rEnd ra
            rb1 = rEnd rb
        in
        if ra1 <= rb0 then
            (a:) <$> go as' bs
        else if rb1 <= ra0 then
            (b:) <$> go as bs'
        else do
            tell [(a,b)]
            if ra0 < rb0 || (ra0 == rb0 && ra1 <= rb1) then
            (a:) <$> go as' bs
            else
            (b:) <$> go as bs'
example 4:
    main :: IO ()
    main = defaultMain testSuite

    testSuite :: TestTree
    testSuite = testGroup "free-vl" [
        testCase "example usage" $ do
        let res = execWriter $ iterM interpreter $ do
                    logDebug "Hey a debug"
                    n <- randomNumber
                    logInfo ("Got a random number " <> show n)
        res @?= fromList [ (Debug, "Hey a debug")
                        , (Info, "Got a random number 42")
                        ]
    ]
    interpreter :: Effects MyEffects (Writer (Seq (LogLevel, String)))
    interpreter = fakeLogger .:. fakeRNG .:. EmptyE
    fakeLogger :: Logging (Writer (Seq (LogLevel, String)))
    fakeLogger = Logging (\lvl msg -> tell (singleton (lvl, msg)))

example 5: 
    createEmbeddedFont :: FontData -> PDF (PDFReference EmbeddedFont)
    createEmbeddedFont (Type1Data d) = do 
        PDFReference s <-  createContent (tell $ fromByteString d) Nothing 
        return (PDFReference s)
example 6:
    main :: IO ()
    main = hspec $ do
        describe "Combinators" Spec.spec
        describe "data loss rules" $ do
            it "consumes the source to quickly" $ do
                x <- runConduitRes $ CL.sourceList [1..10 :: Int] .| do
                    strings <- CL.map show .| CL.take 5
                    liftIO $ putStr $ unlines strings
                    CL.fold (+) 0
                40 `shouldBe` x

            it "correctly consumes a chunked resource" $ do
                x <- runConduitRes $ (CL.sourceList [1..5 :: Int] `mappend` CL.sourceList [6..10]) .| do
                    strings <- CL.map show .| CL.take 5
                    liftIO $ putStr $ unlines strings
                    CL.fold (+) 0
                40 `shouldBe` x
    ...
    describe "monad transformer laws" $ do
        it "transPipe" $ do
            let source = CL.sourceList $ replicate 10 ()
            let tell' x = tell [x :: Int]

            let replaceNum1 = C.awaitForever $ \() -> do
                    i <- lift get
                    lift $ (put $ i + 1) >> (get >>= lift . tell')
                    C.yield i

            let replaceNum2 = C.awaitForever $ \() -> do
                    i <- lift get
                    lift $ put $ i + 1
                    lift $ get >>= lift . tell'
                    C.yield i

            x <- runWriterT $ runConduit $ source .| C.transPipe (`evalStateT` 1) replaceNum1 .| CL.consume
            y <- runWriterT $ runConduit $ source .| C.transPipe (`evalStateT` 1) replaceNum2 .| CL.consume
            x `shouldBe` y
    ...
    describe "WriterT" $
            it "pass" $
                let writer = W.pass $ do
                    W.tell [1 :: Int]
                    pure ((), (2:))
                in execWriter (runConduit writer) `shouldBe` [2, 1]

    describe "Data.Conduit.Lift" $ do
        it "execStateC" $ do
            let sink = C.execStateLC 0 $ CL.mapM_ $ modify . (+)
                src = mapM_ C.yield [1..10 :: Int]
            res <- runConduit $ src .| sink
            res `shouldBe` sum [1..10]

        it "execWriterC" $ do
            let sink = C.execWriterLC $ CL.mapM_ $ tell . return
                src = mapM_ C.yield [1..10 :: Int]
            res <- runConduit $ src .| sink
            res `shouldBe` [1..10]   
example 7:
    transformTypeFamilies :: ExtraTypeScriptOptions -> Type -> WriterT [ExtraDeclOrGenericInfo] Q Type
    transformTypeFamilies eo@(ExtraTypeScriptOptions {..}) (AppT (ConT name) typ)
    | name `L.elem` typeFamiliesToMapToTypeScript = lift (reify name) >>= \case
        FamilyI (ClosedTypeFamilyD (TypeFamilyHead typeFamilyName _ _ _) eqns) _ -> handle typeFamilyName eqns

    #if MIN_VERSION_template_haskell(2,15,0)
        FamilyI (OpenTypeFamilyD (TypeFamilyHead typeFamilyName _ _ _)) decs -> handle typeFamilyName [eqn | TySynInstD eqn <- decs]
    #else
        FamilyI (OpenTypeFamilyD (TypeFamilyHead typeFamilyName _ _ _)) decs -> handle typeFamilyName [eqn | TySynInstD _name eqn <- decs]
    #endif

        _ -> AppT (ConT name) <$> transformTypeFamilies eo typ
    | otherwise = AppT (ConT name) <$> transformTypeFamilies eo typ
            where
            handle :: Name -> [TySynEqn] -> WriterT [ExtraDeclOrGenericInfo] Q Type
            handle typeFamilyName eqns = do
                name' <- lift $ newName (nameBase typeFamilyName <> "'")

                f <- lift $ newName "f"
    #if MIN_VERSION_template_haskell(2,21,0)
                let inst1 = DataD [] name' [PlainTV f BndrReq] Nothing [] []
    #elif MIN_VERSION_template_haskell(2,17,0)
                let inst1 = DataD [] name' [PlainTV f ()] Nothing [] []
    #else
                let inst1 = DataD [] name' [PlainTV f] Nothing [] []
    #endif
                tell [ExtraTopLevelDecs [inst1]]

                imageTypes <- lift $ getClosedTypeFamilyImage eqns
                inst2 <- lift $ [d|instance (Typeable g, TypeScript g) => TypeScript ($(conT name') g) where
                                    getTypeScriptType _ = $(TH.stringE $ nameBase name) <> "[" <> (getTypeScriptType (Proxy :: Proxy g)) <> "]"
                                    getTypeScriptDeclarations _ = [$(getClosedTypeFamilyInterfaceDecl name eqns)]
                                    getParentTypes _ = $(listE [ [|TSType (Proxy :: Proxy $(return x))|] | x <- imageTypes])
                                |]
                tell [ExtraTopLevelDecs inst2]

                tell [ExtraParentType (AppT (ConT name') (ConT ''T))]

                ret <- transformTypeFamilies eo (AppT (ConT name') typ)
                tell [ExtraConstraint (AppT (ConT ''TypeScript) ret)]
                return ret
                ...
example 8:
    import AbsSyn
    import Control.Monad.Writer
    import Control.Monad.Except
    import Data.List(partition,intersperse)
    import qualified Data.Set as S
    import qualified Data.Map as M    -- XXX: Make it work with old GHC.
    expand_rules :: [Rule] -> Either String [Rule1]
    expand_rules rs = do let (funs,rs1) = split_rules rs
                        (as,is) <- runM2 (mapM (`inst_rule` []) rs1)
                        bs <- make_insts funs (S.toList is) S.empty
                        return (as++bs)
    type RuleName = String
    type Inst     = (RuleName, [RuleName])
    type Funs     = M.Map RuleName Rule
    type Rule1    = (RuleName,[Prod1],Maybe String)
    type Prod1    = ([RuleName],String,Int,Maybe String)
    inst_name :: Inst -> RuleName
    inst_name (f,[])  = f
    inst_name (f,xs)  = f ++ "(" ++ concat (intersperse "," xs) ++ ")"
    -- | A renaming substitution used when we instantiate a parameterized rule.
    type Subst    = [(RuleName,RuleName)]
    type M1       = Writer (S.Set Inst)
    type M2       = ExceptT String M1
    ...
    runM2 :: ExceptT e (Writer w) a -> Either e (a, w)
    runM2 m = case runWriter (runExceptT m) of
                (Left e,_)   -> Left e
                (Right a,xs) -> Right (a,xs)
example 9:
    module Rebase.Control.Monad.Writer
    ( module Control.Monad.Writer,
    )
    where
    import Control.Monad.Writer
example 10:
    -- This is lifting, not direct_use_outer:
    instance CatchIO m => CatchIO (WriterT w m) where
    catchIO m h = WriterT $ runWriterT m `catchIO` \e -> runWriterT (h e)

example 11:
    type FileReceiver m = FilePath -> ConduitM ByteString Void m ()
    ...
    receiveMem :: MonadWriter (Map FilePath L.ByteString) m
            => FileReceiver m
    receiveMem fp = do
        bss <- consume
        lift $ tell $ Map.singleton fp $ L.fromChunks bss
example 12:
    instance (Monoid w, Monad m) => MonadWriter w (RSST r w s m) where
        writer (a,w) = tell w >> return a
        tell w = RSST $ \_ (s, ow) ->
            let nw = ow <> w
            in  return ((), (s, nw))
        listen rw = RSST $ \r (s, w) -> do
            (a, (ns, nw)) <- runRSST' rw r (s, mempty)
            return ((a, nw), (ns, w <> nw))
        pass rw = RSST $ \r (s, w) -> do
            ( (a, fw), (s', w') ) <- runRSST' rw r (s, mempty)
            return (a, (s', w `mappend` fw w'))

example 13:
    ...
    instance (PdfObject a, PdfObject b) => PdfLengthInfo (Either a b) where
    modifyStrict :: (MonadState s m) => (s -> s) -> m ()
    modifyStrict f = do
    s <- get
    put $! (f s)
    -- | A monad where paths can be created
    class MonadWriter Builder m => MonadPath m
    data EmbeddedFont 

    instance PdfObject EmbeddedFont where
    toPDF _ = noPdfObject
    ...
////////////////////////////////////////////////////////////
[
{
"package_id": "equivalence-0.4.1.1",
"package": "equivalence",
"module": "Data.Equivalence.Monad",
"path": "src/Data/Equivalence/Monad.hs",
"comment": "defines a new monad transformer deriving MonadWriter",
"explicit_import": false,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 1,
"writer": 0,
"tell": 0,
"listen": 0,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 0,
"runWriter": 0,
"execWriter": 0,
"mapWriter": 0,
"WriterT": 1,
"runWriterT": 0,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": true,
"direct_use_pure": false,
"direct_use_inner": false,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": false,
"re_export": false
},
"need_review": false
},
{
"package_id": "servant-checked-exceptions-core-2.2.0.1",
"package": "servant-checked-exceptions-core",
"module": "Servant.Checked.Exceptions.Internal.EnvelopeT",
"path": "src/Servant/Checked/Exceptions/Internal/EnvelopeT.hs",
"comment": "The EnvelopeT is an instance of MonadWriter and it specifies tell, listen, writer and pass",
"explicit_import": true,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 2,
"writer": 2,
"tell": 2,
"listen": 2,
"pass": 2,
"listens": 0,
"censor": 0,
"Writer": 0,
"runWriter": 0,
"execWriter": 0,
"mapWriter": 0,
"WriterT": 0,
"runWriterT": 0,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": true,
"direct_use_pure": false,
"direct_use_inner": false,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": true,
"re_export": false
},
"need_review": false
},
{
"package_id": "Agda-2.8.0",
"package": "Agda",
"module": "full.Agda.Syntax.Position",
"path": "src/full/Agda/Syntax/Position.hs",
"comment": "",
"explicit_import": true,
"strict_import": true,
"lazy_import": false,
"api_usage": {
"MonadWriter": 0,
"writer": 0,
"tell": 1,
"listen": 0,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 1,
"runWriter": 0,
"execWriter": 0,
"mapWriter": 0,
"WriterT": 0,
"runWriterT": 0,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": false,
"direct_use_pure": true,
"direct_use_inner": false,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": false,
"re_export": false
},
"need_review": false
},
{
"package_id": "free-vl-0.1.4",
"package": "free-vl",
"module": "Spec",
"path": "test/Spec.hs",
"comment": "",
"explicit_import": true,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 0,
"writer": 0,
"tell": 1,
"listen": 0,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 2,
"runWriter": 0,
"execWriter": 1,
"mapWriter": 0,
"WriterT": 0,
"runWriterT": 0,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": false,
"direct_use_pure": true,
"direct_use_inner": true,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": false,
"re_export": false
},
"need_review": false
},
{
"package_id": "HPDF-1.7",
"package": "HPDF",
"module": "Graphics.PDF.Pages",
"path": "Graphics/PDF/Pages.hs",
"comment": "Direct use of tell to write the content of a pdf file",
"explicit_import": false,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 0,
"writer": 0,
"tell": 1,
"listen": 0,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 0,
"runWriter": 0,
"execWriter": 0,
"mapWriter": 0,
"WriterT": 0,
"runWriterT": 0,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": false,
"direct_use_pure": false,
"direct_use_inner": true,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": false,
"re_export": false
},
"need_review": false
},
{
"package_id": "conduit-1.3.6.1",
"package": "conduit",
"module": "main",
"path": "test/main.hs",
"comment": "",
"explicit_import": true,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 0,
"writer": 0,
"tell": 6,
"listen": 1,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 1,
"runWriter": 0,
"execWriter": 2,
"mapWriter": 0,
"WriterT": 0,
"runWriterT": 2,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": false,
"direct_use_pure": true,
"direct_use_inner": true,
"direct_use_middle": false,
"direct_use_outer": true,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": false,
"re_export": false
},
"need_review": false
},
{
"package_id": "aeson-typescript-0.6.4.0",
"package": "aeson-typescript",
"module": "Data.Aeson.TypeScript.Transform",
"path": "src/Data/Aeson/TypeScript/Transform.hs",
"comment": "",
"explicit_import": false,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 0,
"writer": 0,
"tell": 4,
"listen": 0,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 0,
"runWriter": 0,
"execWriter": 0,
"mapWriter": 0,
"WriterT": 2,
"runWriterT": 0,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": false,
"direct_use_pure": false,
"direct_use_inner": false,
"direct_use_middle": false,
"direct_use_outer": true,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": false,
"re_export": false
},
"need_review": false
},
{
"package_id": "happy-meta-0.2.1.0",
"package": "happy-meta",
"module": "ParamRules",
"path": "src/ParamRules.hs",
"comment": "Writer wrapped by ExceptT for logs with error handling",
"explicit_import": false,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 0,
"writer": 0,
"tell": 1,
"listen": 0,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 2,
"runWriter": 1,
"execWriter": 0,
"mapWriter": 0,
"WriterT": 0,
"runWriterT": 0,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": false,
"direct_use_pure": false,
"direct_use_inner": true,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": true,
"re_export": false
},
"need_review": false
},
{
"package_id": "rebase-1.21.2",
"package": "rebase",
"module": "Rebase.Control.Monad.Writer",
"path": "library/Rebase/Control/Monad/Writer.hs",
"comment": "Re-exports the Control.Monad.Writer module",
"explicit_import": false,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 0,
"writer": 0,
"tell": 0,
"listen": 0,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 0,
"runWriter": 0,
"execWriter": 0,
"mapWriter": 0,
"WriterT": 0,
"runWriterT": 0,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": false,
"direct_use_pure": false,
"direct_use_inner": false,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": false,
"re_export": true
},
"need_review": false
},
{
"package_id": "Agda-2.8.0",
"package": "Agda",
"module": "full.Agda.Utils.IO",
"path": "src/full/Agda/Utils/IO.hs",
"comment": "",
"explicit_import": false,
"strict_import": false,
"lazy_import": false,
"api_usage": {
"MonadWriter": 0,
"writer": 0,
"tell": 0,
"listen": 0,
"pass": 0,
"listens": 0,
"censor": 0,
"Writer": 0,
"runWriter": 0,
"execWriter": 0,
"mapWriter": 0,
"WriterT": 2,
"runWriterT": 2,
"execWriterT": 0,
"mapWriterT": 0
},
"categories": {
"lifting": true,
"direct_use_pure": false,
"direct_use_inner": false,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_use": false,
"constraint_only":false,
"not_used": false,
"with_exceptions": true,
"re_export": false
},
"need_review": false
},
{"index": 121, "package_id": "project-template-0.2.1.0", "package": "project-template", "module": "Text.ProjectTemplate", "path": "lts_downloaded/tar_package/lts-24-37/project-template/project-template-0.2.1.0/Text/ProjectTemplate.hs", "comment": "Uses a polymorphic MonadWriter constraint and tell in receiveMem, but no concrete Writer/WriterT stack appears; none of the direct_use or lifting categories fit cleanly.", "explicit_import": true, "strict_import": false, "lazy_import": false, "api_usage": {"MonadWriter": 1, "writer": 0, "tell": 1, "listen": 0, "pass": 0, "listens": 0, "censor": 0, "Writer": 0, "runWriter": 0, "execWriter": 0, "mapWriter": 0, "WriterT": 0, "runWriterT": 0, "execWriterT": 0, "mapWriterT": 0}, "categories": {"lifting": false, "direct_use_pure": false, "direct_use_inner": false, "direct_use_middle": false, "direct_use_outer": false, "polymorphic_use": true, "constraint_only":false, "not_used": false, "with_exceptions": false, "re_export": false}, "need_review": true
},
{"index": 132, "package_id": "stateWriter-0.4.0", "package": "stateWriter", "module": "Control.Monad.Trans.RSS.Lazy", "path": "lts_downloaded/tar_package/lts-24-37/stateWriter/stateWriter-0.4.0/Control/Monad/Trans/RSS/Lazy.hs", "comment": "Defines a MonadWriter instance for the custom RSST transformer and also defines MonadError/liftCatch for the same transformer. This is not a concrete Writer/WriterT program, and it does not clearly fit the lifting category because it implements writer behavior directly rather than lifting an inner MonadWriter capability.", "explicit_import": false, "strict_import": false, "lazy_import": false, "api_usage": {"MonadWriter": 1, "writer": 1, "tell": 2, "listen": 1, "pass": 1, "listens": 0, "censor": 0, "Writer": 0, "runWriter": 0, "execWriter": 0, "mapWriter": 0, "WriterT": 0, "runWriterT": 0, "execWriterT": 0, "mapWriterT": 0}, "categories": {"lifting": true, "direct_use_pure": true, "direct_use_inner": false, "direct_use_middle": true, "direct_use_outer": false,"polymorphic_use": false, "constraint_only":false, "not_used": false, "with_exceptions": true, "re_export": false}, "need_review": false},

{
  "package_id": "pdf-core-1.0.2",
  "package": "pdf-core",
  "module": "Graphics.PDF.LowLevel.Types",
  "path": "src/Graphics/PDF/LowLevel/Types.hs",
  "comment": "Defines MonadPath class with MonadWriter Builder superclass but never uses MonadWriter methods; constraint-only usage",
  "explicit_import": false,
  "strict_import": false,
  "lazy_import": false,
  "api_usage": {
    "MonadWriter": 1,
    "writer": 0,
    "tell": 0,
    "listen": 0,
    "pass": 0,
    "listens": 0,
    "censor": 0,
    "Writer": 0,
    "runWriter": 0,
    "execWriter": 0,
    "mapWriter": 0,
    "WriterT": 0,
    "runWriterT": 0,
    "execWriterT": 0,
    "mapWriterT": 0
  },
  "categories": {
    "lifting": false,
    "direct_use_pure": false,
    "direct_use_inner": false,
    "direct_use_middle": false,
    "direct_use_outer": false,
    "polymorphic_use": false,
    "constraint_only": true,
    "not_used": false,
    "with_exceptions": false,
    "re_export": false
  },
  "need_review": false
}

]
Do not open, search, or reference other files unless it is necesary for accurate categorization. For example, the following sample of a file doesnt provide enough information to determine the type of use, so you would need to look at the Eff.hs:
    -- | A type of an action to trace.
    data TracedAction action
    = TracedIncomingAction action  -- ^ An action that's about to be handled.
    | TracedIssuedAction action    -- ^ An action that's just been issued by some handler.
    deriving (Eq, Show)

    -- | Pretty print 'TraceActionType'.
    ppTracedAction :: Show action => TracedAction action -> String
    ppTracedAction (TracedIncomingAction action) = "Incoming: " <> ppShow action
    ppTracedAction (TracedIssuedAction   action) = "Issued:   " <> ppShow action

    -- | Trace (debug print) every incoming and issued action.
    traceBotActionsWith
    :: (TracedAction action -> String)  -- ^ How to display an action.
    -> BotApp model action
    -> BotApp model action
    traceBotActionsWith f botApp = botApp { botHandler = newHandler }
    where
        traceAction (Just action) = Just action <$ do
        liftIO $ putStrLn (f (TracedIssuedAction action))
        traceAction Nothing = pure Nothing
        
        newHandler !action model = do
        Eff (tell (map (>>= traceAction) actions))
        pure newModel
        where
            (newModel, actions) = runEff $
            botHandler botApp
                (trace (f (TracedIncomingAction action)) action)
                model

Write which files you explored in the comment column

Return only a valid JSON object with the structure described earlier. No prose, no markdown, no code fences, no explanation.