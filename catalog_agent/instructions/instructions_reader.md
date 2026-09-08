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


The first 3 lines you will receive are 3 lines are metadata (package_id, module, file_path)
and then goes the content of the file. 
The expected output is in Json style like this made-up example:
{
"package_id": "example-0.4.1.1",
"module": "Data.Example.Monad",
"file_path": "src/Data/Example/Monad.hs",
"comment": "",
"explicit_import": false,
"qualified_import": false,
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
"with_writer": false,
"with_state": false,
"with_parser": false,
"with_rws": false,
"re_export": false
},
"need_review": true
}

Where, "package_id", "module" "file_path" are given to you. 
"comment" Its an optional string with a brief comment about the module. Only use when explaining "need_review", noting unusual usage, suggesting new category and reporting ambiguous use cases or difficulty in finding a fitting category. If you inspect another file, it should be noted in the comment. Otherwise just "".
"explicit_import" is a boolean that indicates whether Control.Monad.Reader is imported using an explicit import list. It describes whether an explicit import list is present. It is independent of whether the import is qualified.
Set explicit_import = true when at least one import of Control.Monad.Reader specifies imported names in parentheses.
Set explicit_import = false when Control.Monad.Reader is imported without an explicit import list, or is not imported.
Explicit examples:
    import Control.Monad.Reader (ask, local) -- -> explicit_import = true
    import Control.Monad.Reader (ReaderT(..), runReaderT) -- -> explicit_import = true
    import qualified Control.Monad.Reader as R (ask, ReaderT) -- -> explicit_import = true
Non explicit examples:
    import Control.Monad.Reader -- -> explicit_import = false
    import qualified Control.Monad.Reader as R -- -> explicit_import = false


"qualified_import" indicates whether Control.Monad.Reader is imported using the "qualified" keyword.
Set qualified_import = true when at least one import of Control.Monad.Reader is qualified.
Set qualified_import=false when Control.Monad.Reader is imported only unqualified, or is not imported.
qualified examples:
    import qualified Control.Monad.Reader -- -> qualified_import = true
    import qualified Control.Monad.Reader as R -- -> qualified_import = true
    import qualified Control.Monad.Reader as R (ask, ReaderT) -- -> qualified_import = true
non qualified examples:
    import Control.Monad.Reader -- -> qualified_import = false
    import Control.Monad.Reader (ask, ReaderT) -- -> qualified_import = false

qualified_import describes qualification only. It is independent of whether an explicit import list is present.
"need_review" is a boolean, true if you consider that no category fits properly, or if you lack context or information to properly categorize, or if simply there is something strange in the file. Leaving a brief comment about it in the "comment".
"api_usage" contains an int count for every class, type and function in the Control.Monad.Reader. Should only count the occurrences as they come from the import, for example, redefining "ask" in a nonrelated way no longer counts; although specifying ask in instancing for MonadReader or similar should be counted. Declaration heads, instances heads, method definitions, method usages and type signatures are counted as occurrences. Occurrences in module export lists also count. Do not count the import or explicit import occurrences. Do not count commented or string occurences. A symbol is counted only when syntactically attributable to Control.Monad.Reader, either through its unqualified import binding or through a qualified/aliased import of Control.Monad.Reader
"categories" these are independent boolean properties, so a file might satisfy multiple categories simultaneously. "categories" contains the categories in which the usage of Control.Monad.Reader falls into for this file. A property or category is marked true if it fits the criteria for said category, which are explained below. Also, categories are not necessarily mutually exclusive and that a single file may contain several different uses, resulting in multiple categories being present.

1. lifting_reader:
    Mark lifting_reader = true when Reader-related capabilities are propagated through another monad transformer layer. This includes defining or using MonadReader instances that delegate Reader operations through another transformer, for example:

        instance MonadReader r m => MonadReader r (StateT s m) where
            ask = lift ask
            local f = mapStateT (local f)

    The defining characteristic is that Reader/MonadReader behavior is explicitly lifted or propagated through a transformer layer other than ReaderT itself. Do not mark lifting_reader=true merely because ReaderT appears in an instance definition.

2. lifting_readert: 
    Mark lifting_readert=true when ReaderT itself is being defined or when an instance/capability is being implemented for ReaderT by delegating behavior through the ReaderT layer. This includes:

        instance MonadReader r (ReaderT r m) where
            ask = ReaderT pure
            local f (ReaderT m) = ReaderT $ \r -> m (f r)

    and instances such as:

        instance MonadWriter w m => MonadWriter w (ReaderT r m) where
            tell = lift . tell

        instance (Applicative m, Semigroup a) => Semigroup (ReaderT r m a) where
            (<>) = liftA2 (<>)

    The defining characteristic is that ReaderT is itself the transformer layer whose instance or implementation is being defined.Do not mark direct_use_outer=true merely because such an instance exists. Mark direct_use_outer=true only when the file contains an actual ReaderT computation used as the outer monad layer.

For direct_use_inner, direct_use_middle, and direct_use_outer, classify the
position of the explicit ReaderT layer relative to OTHER transformer layers.

Important:
"inner" does NOT mean "closest to the base monad".
A ReaderT directly over a base monad is still outer if no transformer wraps it.

Determine the position as follows:

a. direct_use_outer
   ReaderT has no transformer layer above it.
   Examples:
     ReaderT R IO
     ReaderT R []
     ReaderT R (StateT S IO)
   -- -> direct_use_outer = true

b. direct_use_middle
   ReaderT has at least one transformer layer above it
   AND at least one transformer layer below it.
   Example:
     StateT S (ReaderT R (ExceptT E IO))
   -- -> direct_use_middle = true

c. direct_use_inner
   ReaderT has at least one transformer layer above it
   AND no transformer layer below it; only the base monad is below ReaderT.
   Examples:
        StateT S (ReaderT R IO)
        WriterT W (ReaderT R [])
    -- -> direct_use_inner = true
    ReaderT R [] is outer, not inner.
    ReaderT R IO is outer, not inner.
For a single concrete ReaderT layer, exactly one of direct_use_inner, direct_use_middle, or direct_use_outer applies. A file may have more than one of these categories true only if it contains multiple distinct ReaderT usages at different positions.

3. direct_use_pure:
    Mark direct_use_pure=true when the Reader computation has no additional effects beyond Reader itself. This includes "Reader r a" and "ReaderT r Identity a".
4. direct_use_inner:
    Mark direct_use_inner=true when an actual Reader/ReaderT computation occupies the inner position according to the positional rule above. 
5. direct_use_middle:
    Mark direct_use_middle=true when an actual Reader/ReaderT computation occupies the middle position according to the positional rule above.
6. direct_use_outer: 
    Mark direct_use_outer when Reader or ReaderT is the outer layer (top of the stack) so the inner effects happen inside the Reader.
    For example, (ReaderT w m a), where m has effects or is a transformer stack. But if just (Reader w a) then it is probably just direct_use_pure=true.
    If ReaderT/runReaderT is used only to define a transformer instance that propagates reader-related behavior through the layer, classify it as lifting_readert=true. Do not mark direct_use_outer=true unless the file contains an actual ReaderT computation whose primary monad is ReaderT ... and not just an instance/lifted behavior definition.
7. polymorphic_use:
    Mark polymorphic_use = true when a function's implementation uses ask, local, reader, or asks (or any concrete Reader/ReaderT operations) within a polymorphic context where the concrete monad is specified only by a MonadReader constraint. The function must actually execute reader operations, not just mention them in type signatures. The actual monad is determined by the caller. This is distinct from constraint_only where the methods aren't actually used.
    A type synonym or alias that expands to a concrete Reader/ReaderT stack does not constitute polymorphic use. For polymorphic_use=true, the function's monad must remain genuinely abstract through a type variable constrained by MonadReader (or equivalent polymorphic context). A function using asks, ask, local, reader, or similar operations in a concrete Reader/ReaderT type or a type synonym that expands to one is not polymorphic_use.
8. constraint_only:
    Mark constraint_only = true when the file references MonadReader (or any of its methods like ask, local, reader, asks) only in type signatures or class constraints, but executes no actual reader operations (no ask, local, reader, or asks calls), uses no concrete reader types (Reader, ReaderT, runReader, withReader, etc.), and defines no instances of MonadReader (that would be lifting). The reader appears solely as a constraint in type class definitions, function signatures, or data type contexts, serving as an API design element or future capability rather than being used for immediate functionality. This category is mutually exclusive with lifting_reader, lifting_readert, polymorphic_use, direct_use_inner,direct_use_middle, direct_use_outer and not_used.
9. not used:
    mark not_used=true when the monad is not used, none of the functions defined by the Control.Monad.Reader are present. No use of class, type, constructor, function, method, or re-export. Also when the file only references reader as qualified Template Haskell quoted names in derive declarations for unrelated. Its expected that here the api_usage counts are 0.
10. re_export:
    Mark re_export=true when any function or target symbol of Control.Monad.Reader are re-exported. Like, for example:
        -- Re-exporting the entire imported module:
        module Foo (module Control.Monad.Reader) where
        import Control.Monad.Reader
        -- Re-exporting individual imported symbols:
        module Foo (ask, ReaderT) where
        import Control.Monad.Reader (ask, ReaderT)
        --Re-exporting an imported qualified module alias:
        module Foo (module R) where
        import qualified Control.Monad.Reader as R

    
General rule for with_* categories:
    A with_* category is true when the Reader-related computation being categorized directly contains, executes, interprets, or is structurally capability-wise combined with the corresponding effect or abstraction.

    A combination can be established by:

    a. Structural combination
    The effect is part of the same Reader/ReaderT-containing monad stack.

    ReaderT Env (StateT S IO) a
        -> with_state = true
        -> with_io = true

    b. Explicit specialization
    A known Reader-containing polymorphic stack is explicitly instantiated
    with the corresponding effect.

    type Stack m a = ReaderT Env m a
    foo :: Stack (Writer W) a
        -> with_writer = true

    c. Shared polymorphic capability
    The same abstract monad has both MonadReader and the corresponding effect
    capability, and the implementation actually uses both.

    foo :: (MonadReader Env m, MonadIO m) => m ()
    foo = do
        env <- ask
        liftIO ...

        -> with_io = true

    d. Reader-based abstraction
    Where applicable, the Reader computation itself may implement the
    corresponding abstraction.

    type Parser a = ReaderT ParseContext (Except ParseError) a

    If Parser is actually used as the parser abstraction:
        -> with_parser = true

    Do not mark a with_* category merely because the corresponding effect,
    typeclass, module, or function occurs elsewhere in the file. It must be
    directly related to the Reader usage being categorized.

    e. Nested effect execution inside a Reader-related computation

    A with_* category may also be established when a computation running in a
    Reader-capable monad explicitly executes, unwraps, or interprets the
    corresponding effect inside that same computation, even when the effect is not
    a constraint on the Reader monad itself and is not structurally beneath
    ReaderT.

    Example:
        foo :: MonadReader Env m => m (Either Error a)
        foo = do
            ...
            runExceptT someExceptTAction

        -- -> with_exceptions = true

    Likewise:
        foo :: MonadReader Env m => m (a, s)
        foo = runStateT someStateAction initialState

        -- -> with_state = true

    provided the effect execution is genuinely part of the Reader-related computation rather than unrelated code elsewhere in the module.

11. with_exceptions:

    Apply the general with_* rule to exception/error-handling effects or
    abstractions, including Except/ExceptT, MonadError, ErrorT, throwError,
    catchError, and equivalent mechanisms.

    Also mark with_exceptions=true when a function that runs, unwraps, or
    interprets a Reader-related computation directly translates its failure
    result into an exception/error abstraction.

    Example:
    runFoo
        :: MonadError E m
        => ReaderT Env Parser a
        -> m a
    runFoo p =
        case runParser (runReaderT p env) of
        Left e  -> throwError e
        Right a -> pure a
    -- -> with_exceptions = true

    Likewise:
    foo :: MonadReader Env m => m (Either E a)
    foo = runExceptT someExceptTAction
    -- -> with_exceptions = true

    Do not mark with_exceptions=true merely because Either, an exception type,
    or error-related functions appear elsewhere in the file. The error handling
    must be directly connected to the Reader-related computation being categorized.

    Either counts only when it is actually used as the error-handling result or
    interpretation of that Reader-related computation, not merely as ordinary data.

12. with_io:
    Apply the general with_* rule to IO functionality, including IO,
    MonadIO/liftIO, and explicit IO specializations.


13. with_writer:
    Apply the general with_* rule to Writer functionality, including
    Writer/WriterT and MonadWriter operations.


14. with_state:
    Apply the general with_* rule to State functionality, including
    State/StateT and MonadState operations.


15. with_parser:
    Apply the general with_* rule to parser functionality or parser
    abstractions. Because parser monads are less standardized than State or Writer, inspect
    type aliases or newtype definitions when necessary to determine whether a
    named monad is actually a parser monad.

16. with_rws:
    true when the Reader usage being categorized directly uses Control.Monad.RWS, Control.Monad.RWS.Lazy, or Control.Monad.RWS.Strict to provide or use Reader functionality. Typical cases are RWS/RWST computations that actually use Reader functionality such as ask, asks, local, or reader.
    Do not mark with_rws for a manually assembled equivalent transformer stack unless the Control.Monad.RWS API itself is involved. RWS/RWST usage may set with_rws=true, but it does not by itself receive direct_use_pure, direct_use_inner, direct_use_middle, or direct_use_outer, because those categories describe the position of an explicit Reader/ReaderT layer.


You are allowed to read other files if it would help make a categorization certain. With a maximum of 5 extra files. Write which extra files you explored in the comment column.

Return only a valid JSON object with the structure described earlier. No prose, no markdown, no code fences, no explanation.