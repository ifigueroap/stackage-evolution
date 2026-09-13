You are categorizing Haskell source code from Stackage packages that imports at least one of the following modules:
    Control.Monad.Reader
    Control.Monad.Reader.Class
Those are the Reader modules in scope and Reader-related usage may be attributable to any of those modules.
The import flags are independent. If multiple Reader modules are imported, mark every applicable flag
Focus only on the usage attributable to those Reader imports. Consider a Reader use whenever an API symbol listed in the synopsis appears in the code and is attributable to one of those imports, provided that the symbol is not hidden by the import or redefined locally. Qualified and aliased uses also count.

Use only source-supported findings. Do not infer hidden types. You may inspect other files from the package when necessary to categorize the file accurately. Inspect only files that are relevant and likely to resolve uncertainty about the categorization.
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

Not every Reader module in scope necessarily exports every API symbol listed in this synopsis. Count an API occurrence only when the symbol is actually attributable to the Reader module imported by the file.

The first 3 lines you will receive are metadata: package_id, module, and file_path. The remaining lines contain the source file.
The expected output is in Json style like this made-up example:
{
"package_id": "example-0.4.1.1",
"module": "Data.Example.Monad",
"file_path": "src/Data/Example/Monad.hs",
"comment": "",
"explicit_import": false,
"qualified_import": false,
"class_import": false,
"api_usage": {
"MonadReader": 1,
"reader": 0,
"ask": 0,
"local": 0,
"asks": 0,
"Reader": 0,
"runReader": 0,
"mapReader": 0,
"withReader": 0,
"ReaderT": 1,
"runReaderT": 0,
"mapReaderT": 0,
"withReaderT": 0
},
"categories": {
"lifting": true,
"lifting_t": false,
"direct_use_pure": false,
"direct_use_inner": false,
"direct_use_middle": false,
"direct_use_outer": false,
"polymorphic_interface_use": false,
"concrete_interface_use": false,
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

Where, "package_id", "module" and "file_path" are given to you. 
"comment" Its an optional string with a brief comment about the module. Only use when explaining "need_review", noting unusual usage, suggesting a new category and reporting ambiguous use cases or difficulty in finding a fitting category. If you inspect another file, it should also be noted in the comment. Otherwise just "".

"explicit_import" is a boolean that indicates whether at least one Reader import uses an explicit import list. The Reader imports considered are the Reader modules in scope. This property is independent of whether the import is qualified.

Set explicit_import=true when at least one of these Reader modules specifies imported names in parentheses.

Examples:
    import Control.Monad.Reader (ask, local)
    import qualified Control.Monad.Reader as R (ask, ReaderT)
In all of these cases, explicit_import=true.

Set explicit_import=false when none of the Reader imports uses an explicit import list.
Examples:
    import Control.Monad.Reader
    import Control.Monad.Reader.Class
    import qualified Control.Monad.Reader as R
If multiple Reader variants are imported, explicit_import=true if at least one of them uses an explicit import list.

"qualified_import" is a boolean that indicates whether at least one Reader import uses the qualified keyword. The Reader imports considered are the Reader modules in scope. This property is independent of whether an explicit import list is present.

Set qualified_import=true when at least one of these Reader modules is imported qualified.
Examples:
    import qualified Control.Monad.Reader
    import qualified Control.Monad.Reader.Class as RC
    import qualified Control.Monad.Reader as R (ask, ReaderT)
In all of these cases, qualified_import=true.

Set qualified_import=false when all Reader imports are unqualified.
Examples:
    import Control.Monad.Reader.Class
    import Control.Monad.Reader (ask)
If multiple Reader variants are imported, qualified_import=true if at least one of them is qualified.

"class_import": Set class_import=true if Control.Monad.Reader.Class is imported at least once. Otherwise, set class_import=false.
Example:
    import Control.Monad.Reader.Class
or:    
    import qualified Control.Monad.Reader.Class as RC
Both give class_import=true.

"need_review" is a boolean, true if you consider that no category fits properly, or if you lack context or information to properly categorize, or if simply there is something strange in the file. Leaving a brief comment about it in the "comment".

"api_usage" contains an int count for every listed API symbol attributable to the Reader-related imports stated at the beginning of these instructions. Should only count the occurrences as they come from the import, for example, redefining `ask` in an unrelated way does not count; although defining `ask`, `local`, or `reader` as methods of a MonadReader instance does count. Declaration heads, instances heads, method definitions, method usages and type signatures are counted as occurrences. Occurrences in module export lists also count. Do not count the import or explicit import occurrences. Do not count commented or string occurences. A symbol is counted only when syntactically attributable to any of the Reader modules in scope, either through an unqualified import binding or through a qualified/aliased import of any of the Reader modules in scope.

"categories" these are independent boolean properties.A file might satisfy multiple categories simultaneously. "categories" contains the categories in which the usage of Reader monad falls into for this file. A property or category is marked true if it fits the criteria for said category, which are explained below. Also, categories are not necessarily mutually exclusive and that a single file may contain several different uses, resulting in multiple categories being present.

1. lifting:
    Mark lifting=true when a transformer or wrapper other than ReaderT is given MonadReader capability by explicitly forwarding one or more Reader operations to an underlying monad that already provides MonadReader. For example:

        instance MonadReader r m => MonadReader r (MyT m) where
            ask = lift ask
            local f = mapMyT (local f)
    Here the MyT transformer is receiving Reader capability from m, so lifting=true.
    Do not mark it when ReaderT itself is the transformer layer being implemented; that belongs to lifting_t.
    Also do not mark lifting=true merely because a newtype or application wrapper around ReaderT derives or exposes the MonadReader capability supplied by that ReaderT. For example:
        newtype AppT m a = AppT { unAppT :: ReaderT Env m a }
            deriving (Monad, MonadReader Env)
    This alone does not establish lifting=true; Reader is the capability of the wrapped ReaderT rather than a capability being forwarded from an underlying monad through another transformer.

2. lifting_t: 
    Mark lifting_t=true when ReaderT itself is the transformer layer whose implementation or instances are being defined. This includes implementing MonadReader for ReaderT, or giving ReaderT another capability by forwarding operations to its underlying monad:
        instance MyMonadClass m => MyMonadClass (ReaderT r m) where
            myMethod = lift myMethod
            myOtherMethod = mapReaderT myOtherMethod
    Here ReaderT is the transformer receiving the capability, so lifting_t=true.
    If the file defines or implements MonadReader for ReaderT, also counts as lifting_t=true:
        instance Monad m => MonadReader r (ReaderT r m) where
            ask = ReaderT return
            local f (ReaderT m) = ReaderT $ \r -> m (f r)
    Do not mark direct_use_inner, direct_use_middle, or direct_use_outer merely because ReaderT appears in such an instance. Those categories require an actual ReaderT computation used as part of the program's computation stack.


For direct_use_inner, direct_use_middle, and direct_use_outer, classify the position of a concrete ReaderT computation relative to other transformer layers. Generic instances whose purpose is to define, lift, or forward behavior through ReaderT are not direct uses.
A ReaderT occurrence in an instance head does not by itself establish a direct-use category. Mark a direct-use category only when ReaderT is being used as an actual computation stack, not merely when an instance or capability is being implemented for ReaderT.
3. direct_use_pure:
    Mark direct_use_pure=true when an actual Reader computation has no effects other than Reader itself. So we would see things like `Reader r a` or `ReaderT r Identity a`. A simple example would be:
        getPort :: Reader Config Int
        getPort = asks configPort

    Do not mark direct_use_inner, direct_use_middle, or direct_use_outer solely because of a pure Reader or `ReaderT r Identity` computation.

4. direct_use_inner:
    Mark direct_use_inner=true when an actual ReaderT computation has at least one transformer layer above it, but no transformer layer below it; only a base monad is underneath ReaderT. So things like `StateT S (ReaderT Env IO)` and `ReaderT Env (ReaderT Env [])` make direct_use_inner=true. An example:
        type MyStack = StateT Int (ReaderT Config IO)
        readConfig :: MyStack Config
        readConfig = lift ask
    Here another transformer wraps ReaderT, while only the base monad is below ReaderT.

5. direct_use_middle:
    Mark direct_use_middle=true when an actual ReaderT computation has at least one transformer layer above it and at least one transformer layer below it. For example:
        type MyStack = StateT Int (ReaderT Config (ExceptT String IO))
        readConfig :: MyStack Config
        readConfig = lift ask
    StateT is above ReaderT, and ExceptT is below it, therefore direct_use_middle=true. Note that we use the word "middle" loosely, as we dont care if there are more layers above or below, only that there is at least one above and one below.


6. direct_use_outer:
    Mark direct_use_outer=true when an actual ReaderT computation has no transformer layer above ReaderT. The monad underneath ReaderT may be a base monad or another transformer stack. Like so:
        ReaderT Env IO
        ReaderT Env []
        ReaderT Env (StateT S IO)
    In all three cases, ReaderT is the outermost transformer layer.
    An example of direct_use_outer=true would be:
        type MyStack = ReaderT Config IO
        runTask :: MyStack ()
        runTask = do
            cfg <- ask
            liftIO (print cfg)
    A ReaderT directly over a base monad and with no transformer layer above it, such as ReaderT Env IO, then is outer, not inner.

In polymorphic_interface_use and concrete_interface_use, “interface” refers to the corresponding effect typeclass (in this case is MonadReader).
7. polymorphic_interface_use:
    Mark polymorphic_interface_use=true when an ordinary function or computation runs in a genuinely abstract monad constrained by MonadReader, and its implementation actually uses Reader operations such as reader, ask, local or asks.
    Example:
        getMode :: MonadReader Env m => m Mode
        getMode = asks envMode
    Here the concrete monad is not fixed; it is chosen by the caller, and the function actually uses Reader functionality, so polymorphic_interface_use=true.

    A type synonym or newtype that expands to a concrete Reader/ReaderT stack does not count as polymorphic use merely because the underlying implementation is hidden.

    Do not mark polymorphic_interface_use=true for MonadReader instance implementations whose purpose is to lift or forward Reader behavior through a transformer or wrapper. Those belong to the lifting or lifting_t categories.

    Reader operations used inside an instance method of some unrelated class still count as polymorphic_interface_use when the method runs in an abstract MonadReader-constrained monad. Only MonadReader instance implementations whose purpose is forwarding/lifting are excluded.

8. concrete_interface_use:
    Set concrete_interface_use=true when Reader operations such as
    reader, ask, local or asks are used in a
    specific concrete monad type that has a MonadReader instance, but the
    computation is not implemented as Reader or ReaderT.

    This category is for concrete monads that provide Reader functionality
    through a MonadReader instance.
    Example:
        newtype MyMonad a = MyMonad ...
        instance MonadReader Config MyMonad where
            ask = ...
            local = ...

        foo :: MyMonad Config
        foo = ask

    Here foo uses Reader functionality in the concrete monad MyMonad, therefore concrete_interface_use=true.
    Defining the MonadReader instance itself does not by itself establish concrete_interface_use; there must be an ordinary computation using the interface in that concrete monad.

    The MonadReader instance may be defined in another module. If necessary,
    inspect the relevant definition to establish that the concrete monad has a
    MonadReader instance.
    A concrete wrapper around Reader or ReaderT may satisfy both a direct_use_* category and concrete_interface_use.

    The direct_use_* category describes the underlying Reader/ReaderT computation stack after expanding transparent type aliases or newtype wrappers.

    concrete_interface_use describes how ordinary computations use Reader
    operations through a distinct concrete monad type's MonadReader instance.
    For example:
        newtype App a = App (ReaderT Env IO a)
        deriving (Functor, Applicative, Monad, MonadReader Env)

        foo :: App Env
        foo = ask
    Here:
        direct_use_outer=true
        concrete_interface_use=true

    because App is concretely implemented using ReaderT Env IO, while foo uses the Reader interface through the distinct concrete type App.

    Likewise:
        newtype Query s a = Query (Reader s a)deriving (MonadReader s)
        foo :: Query S S
        foo = ask
    gives:
        direct_use_pure=true
        concrete_interface_use=true

    Only suppress concrete_interface_use when the computation itself has type Reader ... or ReaderT ..., rather than a distinct concrete wrapper type.
    Do not mark concrete_interface_use=true merely because a concrete monad has a MonadReader instance. Reader operations must actually be used in the computation being classified.

9. constraint_only:
    Mark constraint_only=true when MonadReader appears only as a type-level requirement, such as in a function signature, class constraint, or data/type declaration, but the file does not actually execute Reader operations and does not use a concrete Reader or ReaderT computation.

    Example:

        foo :: MonadReader [String] m => Int -> m Int
        foo x = pure (x + 1)

    Here MonadReader is required by the type signature, but no Reader operation such as reader, ask, local or asks is used, so constraint_only=true.

    Do not mark constraint_only=true if the file:

    - actually executes Reader operations,
    - uses concrete Reader/ReaderT computations or runners,
    - defines a MonadReader instance,
    - or re-exports Reader API.

    constraint_only is mutually exclusive with the lifting, lifting_t, polymorphic_interface_use, concrete_interface_use, the direct-use categories, and not_used categories.

    For abstract MonadReader-constrained code:
    if Reader operations are actually executed -> polymorphic_interface_use
    if MonadReader is only required at the type/API level -> constraint_only

10. not_used:
    Mark not_used=true when the file imports any of the Reader modules in scope, but contains no attributable use of any Reader API symbol from that import.

    This means there is no use of MonadReader, reader, ask, local, asks, Reader, runReader, mapReader, withReader, ReaderT, runReaderT, mapReaderT or withReaderT. In this case, all api_usage counts should be 0.

    Do not count:
    - the import declaration itself,
    - occurrences in comments or string literals,
    - unrelated local definitions that reuse names such as reader or ask,
    - names that are hidden by the import,
    - qualified Template Haskell names that do not refer to the imported Reader API.
    not_used is mutually exclusive with every other Reader-usage category, including re_export.

    example of re_export=true and not_used=false:
        module Foo (ask) where
        import Control.Monad.Reader (ask)
        ... -- file continues without further use of the Reader API. Then api_usage counts are all 0 except for ask=1.

11. re_export:
    Mark re_export=true when the module exports any symbol that comes from any of the Reader modules in scope, either by re-exporting the whole imported module or by exporting individual imported Reader API symbols.
    Example:
        module Foo (ask) where
        import Control.Monad.Reader (ask)

    In these cases, re_export=true. Export-list occurrences of individual Reader API symbols also count toward api_usage.

    Do not mark re_export=true merely because a locally defined function with the same name as a Reader API symbol is exported; the exported symbol must actually come from the Reader import.

General rule for with_* categories: A with_* category is true when the Reader-related computation directly contains, executes, interprets, or is structurally combined with the corresponding effect or abstraction (* can be io, writer, state, parser, rws or exceptions; they will be explained shortly after this section). A combination can be established by:
a. Structural combination:
    The corresponding * effect is part of the same monad stack that contains Reader or ReaderT. For example:
        type App = ReaderT [String] (StateT Int IO)

    This directly establishes with_state=true and with_io=true
    The important point is that the effect is part of the same stack, not merely somewhere else in the module.

    If the base monad is a project-defined alias or newtype and its relevant capabilities cannot be determined from the current file, inspect its definition when necessary. Expand it far enough to establish source-supported capabilities of the concrete Reader computation. For example:
        type App = ReaderT Env CustomM
    If inspection establishes that CustomM provides mutable State, MonadError Error, and IO as capabilities of this concrete computation, then with_state=true, with_exceptions=true, and with_io=true. Do not stop merely because the base monad is a custom abstraction.

b. Explicit specialization:
    A polymorphic stack is explicitly instantiated with another effect, making the resulting computation involve Reader/ReaderT and another effect *.
    Example:
        type MyStack m a = ReaderT Env m a
        foo :: MyStack (Writer Log) ()
    Here the alias expands to a concrete Reader + Writer stack, therefore with_writer=true.
    We could also have something like:
        type MyStack m a = StateT Int m a
        foo :: MyStack (Reader [String]) ()
    Where the alias expands to a concrete State + Reader stack, therefore with_state=true.

    Follow type aliases through concrete type arguments even when the
    specialization appears inside another type or API signature.
    For example:
        type Run m = StateT S (ReaderT Env m)
        makeContext :: Context (Run (Writer Log))
    establishes with_writer=true if this specialized Run computation is genuinely part of the API/computation being defined or used.

c. Shared polymorphic capability:
    The same abstract monad has both MonadReader and * capability, and the implementation actually uses operations from both capabilities. For example:
        foo :: (MonadReader Env m, MonadIO m) => m ()
        foo = do
            env <- ask
            liftIO ...
    Therefore with_io=true

    Merely having both constraints in the type signature is not sufficient. The function body must actually use Reader functionality and the corresponding capability.
    Effect usage may be direct, or through a called operation whose exposed type/signature explicitly requires the corresponding effect capability or whose API purpose explicitly performs that effect. Incidental implementation details hidden inside otherwise unrelated helpers do not count.


d. Nested effect execution:
    A with_* category may also be true when a computation running in a Reader-capable monad explicitly runs or interprets another effect inside that same computation, even if that effect is not structurally part of the Reader stack.
    Example:
        parser :: ExceptT Error m Int
        foo :: MonadReader Env m => m (Either Error Int)
        foo = do
            _ <- ask
            runExceptT parser
    Then with_exceptions=true

    Likewise:
        stateful :: StateT State m Int

        foo :: MonadReader Env m => m (Int, State)
        foo = do
            _ <- ask
            runStateT stateful initialState
    gives with_state=true

e. Polymorphic effect specialization:
    A with_* category is also true when a polymorphic computation that explicitly performs the corresponding effect is concretely instantiated with a Reader/ReaderT-containing monad, and that specialization is actually used, executed, or tested. Merely defining an unused compatible Reader-specialized value is not sufficient.

Do not mark a with_* category merely because the corresponding module, typeclass, type, or function appears elsewhere in the file. The effect must be directly related to the Reader computation being categorized. Do not infer combinations from effects hidden inside imported helper functions. If you need to read other files in the module in order to categorize precisely, you must do so.

12. with_exceptions:
    Mark with_exceptions=true when Reader is directly combined with exception handling according to the general with_* rule. This includes stacks such as:
        ReaderT Env (ExceptT Error IO)
        ExceptT Error (ReaderT Env IO)

    It also includes polymorphic code where the same abstract monad actually uses both Reader and exception capabilities:
        foo :: (MonadReader Env m, MonadError Error m) => m ()
        foo = do
            _ <- ask
            throwError err

    And it includes explicitly running or interpreting an exception computation as part of a Reader-related computation:
        computation :: ExceptT Error m Int
        foo :: MonadReader Env m => m (Either Error Int)
        foo = do
            _ <- ask
            runExceptT computation

    Do not mark with_exceptions=true merely because exception-related types or functions appear elsewhere in the file and are unrelated to the Reader computation.

    Exception handling is semantic and is not restricted to Except/ExceptT or MonadError. It also includes exception APIs such as Control.Exception, MonadThrow, MonadCatch, MonadMask, throwM, catch, try, mask, finally, throwIO, catchIO, and equivalent project-specific abstractions.

    If a Reader computation is run inside such exception handling, or such
    exception handling is used to execute/control the Reader computation,
    with_exceptions=true.
    For example:
        foo :: ReaderT Env IO a -> IO (Either SomeException a)
        foo r = try (runReaderT r env)
    gives with_exceptions=true.

    The combination is symmetric with respect to interpretation. It also counts when an exception-capable computation runs/interprets a Reader computation:
        foo :: MonadError Error m => ReaderT Env Parser a -> m a
        foo r =
            case runParser (runReaderT r env) of
                Left err -> throwError err
                Right x  -> pure x
    Here with_exceptions=true.

    If a generic exception test/computation is actually instantiated and executed with ReaderT, the combination counts.
    For example:
        testCatch :: MonadCatch m => MSpec m -> ...
        readerSpec :: MSpec (ReaderT Env IO)
    If testCatch is actually run using readerSpec, then with_exceptions=true.
13. with_io:
    Mark with_io=true when Reader is directly combined with IO according to the general with_* rule. This includes stacks such as:
        ReaderT Env IO
        StateT S (ReaderT Env IO)
        ReaderT Env (ReaderT Env IO)

    It also includes polymorphic code where the same abstract monad actually uses both Reader and IO capabilities:
        foo :: (MonadReader Env m, MonadIO m) => m ()
        foo = do
            env <- ask
            liftIO (print env)

    In this case, with_io=true because the computation actually uses both Reader functionality and IO functionality.
    Do not mark with_io=true merely because MonadIO appears in a constraint, or because IO-related code appears elsewhere in the file without being part of the Reader-related computation.


14. with_writer: Mark with_writer=true when Reader is directly combined with Writer according to the general with_* rule. This includes concrete stacks such as:
        ReaderT Env (WriterT Log IO)
        WriterT Log (ReaderT Env IO)

    It also includes explicit specialization:
        type Stack m a = ReaderT Env m a
        foo :: Stack (Writer Log) ()

    and the reverse:
        type Stack m a = WriterT Log m a
        foo :: Stack (Reader Env) ()

    It also includes polymorphic code where the same abstract monad actually uses both Reader and Writer functionality:
        foo :: (MonadReader Env m, MonadWriter Log m) => m ()
        foo = do
            env <- ask
            tell [show env]

    Do not mark with_writer=true merely because MonadWriter, Writer, WriterT, tell, or related Writer code appears elsewhere in the file without being directly related to the Reader computation.

15. with_state:
    Mark with_state=true when Reader is directly combined with State according to the general with_* rule. This includes concrete stacks such as:
        ReaderT Env (StateT S IO)
        StateT S (ReaderT Env IO)

    It also includes explicit specialization in either direction:
        type Stack m a = ReaderT Env m a
        foo :: Stack (State S) ()

    or:
        type Stack m a = StateT S m a
        foo :: Stack (Reader Env) ()

    It also includes polymorphic code where the same abstract monad actually uses both Reader and State functionality:
        foo :: (MonadReader Env m, MonadState S m) => m ()
        foo = do
            _ <- ask
            modify update

    Do not mark with_state=true merely because MonadState, State, StateT, get, put, modify, or other State-related code appears elsewhere in the file without being directly related to the Reader computation.

16. with_parser:
    Mark with_parser=true when Reader is directly combined with a parser computation according to the general with_* rule.

    This includes concrete stacks where a parser transformer and Reader are part of the same computation stack, for example:
        ReaderT Env (ParsecT e s m)
        ParsecT e s (ReaderT Env m)

    It also includes explicit specialization:
        type Stack m a = ReaderT Env m a
        foo :: Stack (Parsec e s) Result

    or the reverse:
        type ParserT m a = ParsecT e s m a
        foo :: ParserT (Reader Env) Result

    It can also apply when a Reader-related computation explicitly runs or interprets a parser computation as part of its work:
        foo :: MonadReader Env m => Input -> m (Either ParseError Result)
        foo input = do
            _ <- ask
            pure (parse parser "" input)

    Parser functionality is semantic and is not restricted to standard parser libraries. A Reader-based abstraction that is explicitly defined and used as a parser also counts. For example:
        -- | The Parser monad.
        type Parser a = ReaderT ParseContext (Except ParseError) a
    If this abstraction is actually used by parsing operations and a parser runner, then with_parser=true.

    Do not mark with_parser=true merely because parser-related imports, parser types, or parsing functions occur elsewhere in the file without being directly related to the Reader computation.


17. with_rws:
    Mark with_rws=true when Reader is directly combined with an RWS computation according to the general with_* rule. This includes concrete stacks such as:
        ReaderT Env (RWST Env W S IO)
        RWST Env W S (ReaderT Env IO)

    It also includes explicit specialization:
        type Stack m a = ReaderT Env m a
        foo :: Stack (RWS Env W S) ()

    or the reverse:
        type Stack m a = RWST Env W S m a
        foo :: Stack (Reader Log) ()
    
    Because RWS/RWST intrinsically combines Reader, Writer, and State effects, actual RWS/RWST usage may also establish with_writer=true and with_state=true when those effects are directly part of the Reader-related computation.
    with_rws does not subsume with_writer or with_state. Evaluate them independently: actual Writer functionality such as tell may establish with_writer=true, and actual State functionality such as get, put, or modify may establish with_state=true.
    Do not mark with_rws=true merely because Reader, Writer, and State capabilities happen to appear separately in the same file. The Reader-related computation must be directly combined with an actual RWS/RWST computation or abstraction.

You are allowed to read other files if it would help make a categorization certain. Write which extra files you explored in the comment column.

Return only a valid JSON object with the structure described earlier. No prose, no markdown, no code fences, no explanation.















