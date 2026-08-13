You are categorizing a Haskell source code from Stackage packages that features the Control.Monad.Writer import. 
Focus only on the usage of the Control.Monad.Writer. You will consider a use of Control.Monad.Writer everytime a function of said module appears in the code, 
without it being hidden at import or redefined. Also should consider use when the module is aliased or qualified.
You shall use only source-supported findings. Do not infer hidden types. Explain uncertainty in comment.
This is the synopsis of Control.Monad.Writer from https://hackage-content.haskell.org/package/mtl-2.3.2/docs/Control-Monad-Writer-Lazy.html

class (Monoid w, Monad m) => MonadWriter w (m :: Type -> Type) | m -> w where

    writer :: (a, w) -> m a
    tell :: w -> m ()
    listen :: m a -> m (a, w)
    pass :: m (a, w -> w) -> m a

listens :: MonadWriter w m => (w -> b) -> m a -> m (a, b)
censor :: MonadWriter w m => (w -> w) -> m a -> m a
type Writer w = WriterT w Identity
runWriter :: Writer w a -> (a, w)
execWriter :: Writer w a -> w
mapWriter :: ((a, w) -> (b, w')) -> Writer w a -> Writer w' b
newtype WriterT w (m :: Type -> Type) a = WriterT (m (a, w))
runWriterT :: WriterT w m a -> m (a, w)
execWriterT :: Monad m => WriterT w m a -> m w
mapWriterT :: (m (a, w) -> n (b, w')) -> WriterT w m a -> WriterT w' n b
module Control.Monad.Trans


The first 4 lines you will receive are 4 lines are metadata (package, module, path)
and then goes the content of the file. 
The expected output is in Json style like this example:
{
"package_id": "equivalence-0.4.1.1"
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
"direct_use_outer": false,
"not_used": false,
"with_exceptions": false,
"re_export": false
},
"need_review": true
}

Where, "package_id", "package", "module" "path" are given to you. 
"comment" Its an optional string with a brief comment about the module. Only use when explaining "need_review", noting unusual usage, suggesting new category reporting ambiguous use cases. Otherwise just "".
"explicit_import" this is a boolean, true if the functions of the module are imported explicitly using an import list (for example: import Control.Monad.Writer ( WriterT )), false if not.
"strict_import" is a boolean, true if the import was the Strict version of the module, like Control.Monad.Writer.Strict and its false otherwise.
"lazy_import" is a boolean, true if the import was the Lazy version of the module, like Control.Monad.Writer.Lazy and its false otherwise.
"need_review" is a boolean, true if you consider that no category fits properly, or if you lack context or information to properly categorize, or if simply there is something strange in the file. Leaving a brief comment about it in the "comment".
"api_usage" contains an int count for every function in the Control.Monad.Writer. Should only count the occurrences as they come from the import, for example, redefining "tell" in a nonrelated way no longer counts; although specifying tell in instancing for MonadWriter or similar should be counted. Type signatures are counted as occurrences. Do not count the import or explicit import occurrences.
"categories" these are independent boolean properties, so a file might satisfy multiple categories simultaneously. "categories" contains the categories in which the usage of Control.Monad.Writer falls into for this file. A property or category is marked true if it fits the criteria for said category, which are explained later. Also mention that categories are not necessarily mutually exclusive and that a single file may contain several different uses, resulting in multiple categories being present.

There are 7 categories, and a file may present multiple categories (examples dont show the full file, only the Control.Monad.Writer related parts)
Here are the categories with examples:
1. lifting: This category is about making capabilities from the inner monad available in outer transformer layers, 
            usually defines how tell passes through a transformer layer, maintaning capability through transformer stacks.
            Mark lifting=true when there is a mechanism that propagates or lifts MonadWriter capabilities from an inner to an outer monad.
            Additionally, ordinary cases like this {foo = lift $ tell ["x"]} fall more under direct_use than lifting.
            If WriterT/runWriterT appears only in an instance that lifts behavior through the transformer layer, classify it as lifting=true and do not mark direct_use_outer=true unless there is an actual concrete WriterT program used as the outer monad stack in the file.
2. direct use (pure): Mark direct_use_pure=true when using Writer or WriterT as the only monad layer with no transformer stack and no effects.
                      So (Writer w) (WriterT w Identity) and aliases of them can be classified as pure.
3. direct use (inner): Writer or WriterT is at the bottom of the stack, and there should be at least one layer wrapping it. So that the log persists through effects  
4. direct use (outer):  Mark direct_use_outer when Writer or WriterT is the outer layer (top of the stack) so the inner effects happen inside the Writer.
                        For example, (WriterT w m a), where m has effects or is a transformer stack. But if just (Writer w a) then it is probably just direct_use_pure=true.
                        If WriterT/runWriterT is used only to define a transformer instance that propagates writer-related behavior through the layer, classify it as lifting=true. Do not mark direct_use_outer=true unless the file contains an actual concrete computation whose primary monad is WriterT ... and not just an instance/lifted behavior definition.       
5. Not used:  mark not_used=true when the monad is not used, none of the functions defined by the Control.Monad.Writer are present. No use of class, type, constructor, function, method, or re-export.
              Its expected that here the api_usage counts are 0.
6. With Exeptions:  Mark with_exceptions=true when Writer related computations are directly combined or used along side with some exception, error handling or exception-catching operations such as ExceptT, MonadError, Either, ErrorT or similar.
                    Do not set it merely because an error-related module is imported or an unrelated error type appears elsewhere in the file
7. Re-export: Mark re_export=true when any function or target symbol of Control.Monad.Writer are re-exported.

--------  examples ---------
Here are 9 examples and after all of them there is a list with the expected outputs. The (...) notes there is a chunk of code there, that has no presence of writer activity.
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
"direct_use_outer": false,
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
"direct_use_outer": false,
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
"direct_use_outer": false,
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
"direct_use_outer": false,
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
"direct_use_outer": false,
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
"direct_use_outer": true,
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
"direct_use_outer": true,
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
"direct_use_outer": false,
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
"direct_use_outer": false,
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
"direct_use_outer": false,
"not_used": false,
"with_exceptions": true,
"re_export": false
},
"need_review": false
}
]
Only inspect the file at file_path. Do not open, search, or reference other files unless absolutely necessary.
Return only a valid JSON object with the above structure. No prose, no markdown, no code fences, no explanation.