You are categorizing Haskell source code from Stackage packages that imports at least one of the following modules:
    Control.Monad.Writer
    Control.Monad.Writer.Lazy
    Control.Monad.Writer.Strict
    Control.Monad.Writer.Class
    Control.Monad.Writer.CPS
Those are the Writer modules in scope and Writer-related usage may be attributable to any of those modules.
The import flags are independent. If multiple Writer modules are imported, mark every applicable flag
Focus only on the usage attributable to those Writer imports. Consider a Writer use whenever an API symbol listed in the synopsis appears in the code and is attributable to one of those imports, provided that the symbol is not hidden by the import or redefined locally. Qualified and aliased uses also count.

Use only source-supported findings. Do not infer hidden types. You may inspect other files from the package when necessary to categorize the file accurately. Inspect only files that are relevant and likely to resolve uncertainty about the categorization.
This is the synopsis of Control.Monad.Writer:

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

Not every Writer module in scope necessarily exports every API symbol listed in this synopsis. Count an API occurrence only when the symbol is actually attributable to the Writer module imported by the file. Uses of Writer and WriterT from Control.Monad.Writer.CPS are concrete Writer computations and are categorized using the same direct_use_* rules.

The first 3 lines you will receive are metadata: package_id, module, and file_path. The remaining lines contain the source file.
The expected output is in Json style like this made-up example:
{
"package_id": "example-0.4.1.1",
"module": "Data.Example.Monad",
"file_path": "src/Data/Example/Monad.hs",
"comment": "",
"explicit_import": false,
"qualified_import": false,
"strict_import": false,
"lazy_import": false,
"class_import": false,
"cps_import": false,
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
"with_reader": false,
"with_state": false,
"with_parser": false,
"with_rws": false,
"re_export": false
},
"need_review": true
}

Where, "package_id", "module" and "file_path" are given to you. 
"comment" Its an optional string with a brief comment about the module. Only use when explaining "need_review", noting unusual usage, suggesting a new category and reporting ambiguous use cases or difficulty in finding a fitting category. If you inspect another file, it should also be noted in the comment. Otherwise just "".

"explicit_import" is a boolean that indicates whether at least one Writer import uses an explicit import list. The Writer imports considered are the Writer modules in scope. This property is independent of whether the import is qualified.

Set explicit_import=true when at least one of these Writer modules specifies imported names in parentheses.

Examples:
    import Control.Monad.Writer (tell, listen)
    import Control.Monad.Writer.Strict (WriterT(..), runWriterT)
    import qualified Control.Monad.Writer.Lazy as W (tell, WriterT)
In all of these cases, explicit_import=true.
Set explicit_import=false when none of the Writer imports uses an explicit import list.

Examples:
    import Control.Monad.Writer
    import Control.Monad.Writer.Strict
    import qualified Control.Monad.Writer.Lazy as W
If multiple Writer variants are imported, explicit_import=true if at least one of them uses an explicit import list.

"qualified_import" is a boolean that indicates whether at least one Writer import uses the qualified keyword. The Writer imports considered are the Writer modules in scope. This property is independent of whether an explicit import list is present.

Set qualified_import=true when at least one of these Writer modules is imported qualified.
Examples:
    import qualified Control.Monad.Writer
    import qualified Control.Monad.Writer.Strict as W
    import qualified Control.Monad.Writer.Lazy as W (tell, WriterT)
In all of these cases, qualified_import=true.

Set qualified_import=false when all Writer imports are unqualified.
Examples:
    import Control.Monad.Writer
    import Control.Monad.Writer.Strict (tell)
    import Control.Monad.Writer.Lazy
If multiple Writer variants are imported, qualified_import=true if at least one of them is qualified.

"strict_import" is a boolean that indicates whether Control.Monad.Writer.Strict is imported. Set strict_import=true if Control.Monad.Writer.Strict appears in at least one import declaration, regardless of whether that import is qualified or uses an explicit import list.
Examples:
    import Control.Monad.Writer.Strict
    import Control.Monad.Writer.Strict (tell)
    import qualified Control.Monad.Writer.Strict as W
In all of these cases, strict_import=true. Otherwise, set strict_import=false.

"lazy_import" is a boolean that indicates whether Control.Monad.Writer.Lazy is imported. Set lazy_import=true if Control.Monad.Writer.Lazy appears in at least one import declaration, regardless of whether that import is qualified or uses an explicit import list.
Examples:
    import Control.Monad.Writer.Lazy
    import Control.Monad.Writer.Lazy (tell)
    import qualified Control.Monad.Writer.Lazy as W
In all of these cases, lazy_import=true. Otherwise, set lazy_import=false.
These import flags are independent. More than one may be true at the same time.
For example:
    import Control.Monad.Writer.Strict (tell)
    import qualified Control.Monad.Writer.Lazy as L
gives:
    explicit_import = true
    qualified_import = true
    strict_import = true
    lazy_import = true


"class_import": Set class_import=true if Control.Monad.Writer.Class is imported at least once. Otherwise, set class_import=false.
Example:
    import Control.Monad.Writer.Class
or:    
    import qualified Control.Monad.Writer.Class as W

    Both give class_import=true.


"cps_import"
    Set cps_import=true if Control.Monad.Writer.CPS is imported at least once. Otherwise, set cps_import=false.
    Example:
        import Control.Monad.Writer.CPS
    or:
        import qualified Control.Monad.Writer.CPS as W
    Both give cps_import=true.


"need_review" is a boolean, true if you consider that no category fits properly, or if you lack context or information to properly categorize, or if simply there is something strange in the file. Leaving a brief comment about it in the "comment".

"api_usage" contains an int count for every listed API symbol attributable to the Writer-related imports stated at the beginning of these instructions. Should only count the occurrences as they come from the import, for example, redefining "tell" in a nonrelated way no longer counts; although specifying tell in instancing for MonadWriter or similar should be counted. Declaration heads, instances heads, method definitions, method usages and type signatures are counted as occurrences. Occurrences in module export lists also count. Do not count the import or explicit import occurrences. Do not count commented or string occurences. A symbol is counted only when syntactically attributable to any of the Writer modules in scope, either through an unqualified import binding or through a qualified/aliased import of any of the Writer modules in scope.

"categories" these are independent boolean properties.A file might satisfy multiple categories simultaneously. "categories" contains the categories in which the usage of Control.Monad.Writer falls into for this file. A property or category is marked true if it fits the criteria for said category, which are explained below. Also, categories are not necessarily mutually exclusive and that a single file may contain several different uses, resulting in multiple categories being present.

1. lifting:
    Mark lifting=true when a transformer or wrapper other than WriterT is given MonadWriter capability by explicitly forwarding one or more Writer operations to an underlying monad that already provides MonadWriter. For example:

        instance MonadWriter w m => MonadWriter w (MyT m) where
            tell = lift . tell
            ...
    Here the MyT transformer is receiving Writer capability from m, so lifting=true.
    Do not mark it when WriterT itself is the transformer layer being implemented; that belongs to lifting_t.

2. lifting_t: 
    Mark lifting_t=true when WriterT itself is the transformer layer whose implementation or instances are being defined. This includes implementing MonadWriter for WriterT, or giving WriterT another capability by forwarding operations to its underlying monad:
        instance MyMonadClass m => MyMonadClass (WriterT w m) where
            myMethod = lift myMethod
            myOtherMethod = mapWriterT myOtherMethod
    Here WriterT is the transformer receiving the capability, so lifting_t=true.
    If the file defines or implements MonadWriter for WriterT, also counts as lifting_t=true:
        instance (Monoid w, Monad m) => MonadWriter w (WriterT w m) where
            tell w = WriterT (return ((), w))
            ...  
    Do not mark direct_use_inner, direct_use_middle, or direct_use_outer merely because WriterT appears in such an instance. Those categories require an actual WriterT computation used as part of the program's computation stack.


For direct_use_inner, direct_use_middle, and direct_use_outer, classify the position of a concrete WriterT computation relative to other transformer layers. Generic instances whose purpose is to define, lift, or forward behavior through WriterT are not direct uses.
A WriterT occurrence in an instance head does not by itself establish a direct-use category. Mark a direct-use category only when WriterT is being used as an actual computation stack, not merely when an instance or capability is being implemented for WriterT.
3. direct_use_pure:
    Mark direct_use_pure=true when an actual Writer computation has no effects other than Writer itself. So we would see things like `Writer w a` or `WriterT w Identity a`. A simple example would be:
        myLog :: Writer [String] ()
        myLog = do
            tell ["my"]
            tell ["log"]

    Do not mark direct_use_inner, direct_use_middle, or direct_use_outer solely because of a pure Writer or `WriterT w Identity` computation.

4. direct_use_inner:
    Mark direct_use_inner=true when an actual WriterT computation has at least one transformer layer above it, but no transformer layer below it; only a base monad is underneath WriterT. So things like `StateT S (WriterT Log IO)` and `ReaderT Env (WriterT Log [])` make direct_use_inner=true. An example:
        type MyStack = StateT Int (WriterT [String] IO)
        buildLog :: MyStack ()
        buildLog = do
            lift $ tell ["my stack"]
    Here another transformer wraps WriterT, while only the base monad is below WriterT.

5. direct_use_middle:
    Mark direct_use_middle=true when an actual WriterT computation has at least one transformer layer above it and at least one transformer layer below it. For example:
        type MyStack = StateT Int (WriterT [String] (ExceptT String IO))
        buildLog :: MyStack ()
        buildLog = do
            lift $ tell ["working"]
    StateT is above WriterT, and ExceptT is below it, therefore direct_use_middle=true. Note that we use the word "middle" loosely, as we dont care if there are more layers above or below, only that there is at least one above and one below.


6. direct_use_outer:
    Mark direct_use_outer=true when an actual WriterT computation has no transformer layer above WriterT. The monad underneath WriterT may be a base monad or another transformer stack. Like so:
        WriterT Log IO
        WriterT Log []
        WriterT Log (StateT S IO)
    In all three cases, WriterT is the outermost transformer layer.
    An example of direct_use_outer=true would be:
        type MyStack = WriterT [String] IO
        myLog :: MyStack ()
        myLog = do
            tell ["starting"]
            liftIO (putStrLn "working")
    A WriterT directly over a base monad and with no transformer layer above it, such as WriterT Log IO, then is outer, not inner.

In polymorphic_interface_use and concrete_interface_use, “interface” refers to the corresponding effect typeclass (in this case is MonadWriter).
7. polymorphic_interface_use:
    Mark polymorphic_interface_use=true when an ordinary function or computation runs in a genuinely abstract monad constrained by MonadWriter, and its implementation actually uses Writer operations such as writer, tell, listen, pass, listens, or censor.
    Example:
        logValue :: MonadWriter [String] m => Int -> m ()
        logValue x = tell [show x]
    Here the concrete monad is not fixed; it is chosen by the caller, and the function actually uses Writer functionality, so polymorphic_interface_use=true.

    A type synonym or newtype that expands to a concrete Writer/WriterT stack does not count as polymorphic use merely because the underlying implementation is hidden.

    Do not mark polymorphic_interface_use=true for MonadWriter instance implementations whose purpose is to lift or forward Writer behavior through a transformer or wrapper. Those belong to the lifting or lifting_t categories.

8. concrete_interface_use:
    Set concrete_interface_use=true when Writer operations such as
    writer, tell, listen, pass, listens, or censor are used in a
    specific concrete monad type that has a MonadWriter instance, but the
    computation is not implemented as Writer or WriterT.

    This category is for concrete monads that provide Writer functionality
    through a MonadWriter instance.
    Example:
        newtype MyMonad a = MyMonad ...
        instance MonadWriter MyWrapper MyMonad where
            tell = ...
            listen = ...
            pass = ...
        foo :: MyWrapper -> MyMonad ()
        foo b = tell b

    Here foo uses Writer functionality in the concrete monad MyMonad, so
    concrete_interface_use=true.
    Defining the MonadWriter instance itself does not by itself establish concrete_interface_use; there must be an ordinary computation using the interface in that concrete monad.

    The MonadWriter instance may be defined in another module. If necessary,
    inspect the relevant definition to establish that the concrete monad has a
    MonadWriter instance.
    Do not mark concrete_interface_use=true when the concrete computation is actually Writer or WriterT; classify those using the appropriate direct_use_* category instead.
    Do not mark concrete_interface_use=true merely because a concrete monad has a MonadWriter instance. Writer operations must actually be used in the computation being classified.
9. constraint_only:
    Mark constraint_only=true when MonadWriter appears only as a type-level requirement, such as in a function signature, class constraint, or data/type declaration, but the file does not actually execute Writer operations and does not use a concrete Writer or WriterT computation.

    Example:

        foo :: MonadWriter [String] m => Int -> m Int
        foo x = pure (x + 1)

    Here MonadWriter is required by the type signature, but no Writer operation such as writer, tell, listen, pass, listens, or censor is used, so constraint_only=true.

    Do not mark constraint_only=true if the file:

    - actually executes Writer operations,
    - uses concrete Writer/WriterT computations or runners,
    - defines a MonadWriter instance,
    - or re-exports Writer API.

    constraint_only is mutually exclusive with the lifting, lifting_t, polymorphic_interface_use, concrete_interface_use, the direct-use categories, and not_used categories.

    For abstract MonadWriter-constrained code:
    if Writer operations are actually executed -> polymorphic_interface_use
    if MonadWriter is only required at the type/API level -> constraint_only

10. not_used:
    Mark not_used=true when the file imports any of the Writer modules in scope, but contains no attributable use of any Writer API symbol from that import.

    This means there is no use of MonadWriter, writer, tell, listen, pass, listens, censor, Writer, runWriter, execWriter, mapWriter, WriterT, runWriterT, execWriterT, or mapWriterT. In this case, all api_usage counts should be 0.

    Do not count:
    - the import declaration itself,
    - occurrences in comments or string literals,
    - unrelated local definitions that reuse names such as writer or tell,
    - names that are hidden by the import,
    - qualified Template Haskell names that do not refer to the imported Writer API.
    not_used is mutually exclusive with every other Writer-usage category, including re_export.

    example of re_export=true and not_used=false:
        module Foo (tell) where
        import Control.Monad.Writer (tell)
        ... -- file continues without further use of the Writer API. Then api_usage counts are all 0 except for tell=1.

11. re_export:
    Mark re_export=true when the module exports any symbol that comes from any of the Writer modules in scope, either by re-exporting the whole imported module or by exporting individual imported Writer API symbols.
    Examples:

        module Foo (module Control.Monad.Writer) where
        import Control.Monad.Writer

        module Foo (tell, WriterT) where
        import Control.Monad.Writer (tell, WriterT)

        module Foo (module W) where
        import qualified Control.Monad.Writer as W

    In these cases, re_export=true. Export-list occurrences of individual Writer API symbols also count toward api_usage.

    Do not mark re_export=true merely because a locally defined function with the same name as a Writer API symbol is exported; the exported symbol must actually come from the Writer import.

General rule for with_* categories: A with_* category is true when the Writer-related computation directly contains, executes, interprets, or is structurally combined with the corresponding effect or abstraction (* can be io, reader, state, parser, rws or exceptions; they will be explained shortly after this section). A combination can be established by:
a. Structural combination:
    The corresponding * effect is part of the same monad stack that contains Writer or WriterT. For example:
        type App = WriterT [String] (StateT Int IO)

    This directly establishes with_state=true and with_io=true
    The important point is that the effect is part of the same stack, not merely somewhere else in the module.

b. Explicit specialization:
A polymorphic stack is explicitly instantiated with another effect, making the resulting computation involve Writer/WriterT and another effect *.
Example:
    type MyStack m a = WriterT [String] m a
    foo :: MyStack (Reader Env) ()
Here the alias expands to a concrete Writer + Reader stack, therefore with_reader=true.
We could also have something like:
    type MyStack m a = StateT Int m a
    foo :: MyStack (Writer [String]) ()
Where the alias expands to a concrete State + Writer stack, therefore with_state=true.


c. Shared polymorphic capability:
    The same abstract monad has both MonadWriter and * capability, and the implementation actually uses operations from both capabilities. For example:
        foo :: (MonadWriter [String] m, MonadIO m) => m ()
        foo = do
            tell ["starting"]
            liftIO (putStrLn "hello")
    Therefore with_io=true

    Merely having both constraints in the type signature is not sufficient. The function body must actually use Writer functionality and the corresponding capability.


d. Nested effect execution:
    A with_* category may also be true when a computation running in a Writer-capable monad explicitly runs or interprets another effect inside that same computation, even if that effect is not structurally part of the Writer stack.
    Example:
        parser :: ExceptT Error m Int
        foo :: MonadWriter [String] m => m (Either Error Int)
        foo = do
            tell ["running parser"]
            runExceptT parser
    Then with_exceptions=true

    Likewise:
        stateful :: StateT State m Int

        foo :: MonadWriter [String] m => m (Int, State)
        foo = do
            tell ["running state"]
            runStateT stateful initialState
    gives with_state=true

Do not mark a with_* category merely because the corresponding module, typeclass, type, or function appears elsewhere in the file. The effect must be directly related to the Writer computation being categorized. Do not infer combinations from effects hidden inside imported helper functions. If you need to read other files in the module in order to categorize precisely, you must do so.

12. with_exceptions:
    Mark with_exceptions=true when Writer is directly combined with exception handling according to the general with_* rule. This includes stacks such as:
        WriterT Log (ExceptT Error IO)
        ExceptT Error (WriterT Log IO)

    It also includes polymorphic code where the same abstract monad actually uses both Writer and exception capabilities:
        foo :: (MonadWriter [String] m, MonadError Error m) => m ()
        foo = do
            tell ["starting"]
            throwError err

    And it includes explicitly running or interpreting an exception computation as part of a Writer-related computation:
        computation :: ExceptT Error m Int
        foo :: MonadWriter [String] m => m (Either Error Int)
        foo = do
            tell ["running"]
            runExceptT computation

    Do not mark with_exceptions=true merely because exception-related types or functions appear elsewhere in the file and are unrelated to the Writer computation.

13. with_io:
    Mark with_io=true when Writer is directly combined with IO according to the general with_* rule. This includes stacks such as:
        WriterT Log IO
        StateT S (WriterT Log IO)
        WriterT Log (ReaderT Env IO)

    It also includes polymorphic code where the same abstract monad actually uses both Writer and IO capabilities:
        foo :: (MonadWriter [String] m, MonadIO m) => m ()
        foo = do
            tell ["starting"]
            liftIO (putStrLn "working")

    In this case, with_io=true because the computation actually uses both Writer functionality and IO functionality.
    Do not mark with_io=true merely because MonadIO appears in a constraint, or because IO-related code appears elsewhere in the file without being part of the Writer-related computation.


14. with_reader:
    Mark with_reader=true when Writer is directly combined with Reader according to the general with_* rule. This includes concrete stacks such as:
        WriterT Log (ReaderT Env IO)
        ReaderT Env (WriterT Log IO)

    It also includes explicit specialization:
        type Stack m a = WriterT Log m a
        foo :: Stack (Reader Env) ()

    and the reverse:
        type Stack m a = ReaderT Env m a
        foo :: Stack (Writer Log) ()

    It also includes polymorphic code where the same abstract monad actually uses both Writer and Reader functionality:
        foo :: (MonadWriter Log m, MonadReader Env m) => m ()
        foo = do
            env <- ask
            tell [show env]

    Do not mark with_reader=true merely because MonadReader, Reader, ReaderT, ask, or related Reader code appears elsewhere in the file without being directly related to the Writer computation.

15. with_state:
    Mark with_state=true when Writer is directly combined with State according to the general with_* rule. This includes concrete stacks such as:
        WriterT Log (StateT S IO)
        StateT S (WriterT Log IO)

    It also includes explicit specialization in either direction:
        type Stack m a = WriterT Log m a
        foo :: Stack (State S) ()

    or:
        type Stack m a = StateT S m a
        foo :: Stack (Writer Log) ()

    It also includes polymorphic code where the same abstract monad actually uses both Writer and State functionality:
        foo :: (MonadWriter Log m, MonadState S m) => m ()
        foo = do
            tell log
            modify update

    Do not mark with_state=true merely because MonadState, State, StateT, get, put, modify, or other State-related code appears elsewhere in the file without being directly related to the Writer computation.

16. with_parser:
    Mark with_parser=true when Writer is directly combined with a parser computation according to the general with_* rule.

    This includes concrete stacks where a parser transformer and Writer are part of the same computation stack, for example:
        WriterT Log (ParsecT e s m)
        ParsecT e s (WriterT Log m)

    It also includes explicit specialization:
        type Stack m a = WriterT Log m a
        foo :: Stack (Parsec e s) Result

    or the reverse:
        type ParserT m a = ParsecT e s m a
        foo :: ParserT (Writer Log) Result

    It can also apply when a Writer-related computation explicitly runs or interprets a parser computation as part of its work:
        foo :: MonadWriter Log m => Input -> m (Either ParseError Result)
        foo input = do
            tell log
            pure (parse parser "" input)

    Do not mark with_parser=true merely because parser-related imports, parser types, or parsing functions occur elsewhere in the file without being directly related to the Writer computation.


17. with_rws:
    Mark with_rws=true when Writer is directly combined with an RWS computation according to the general with_* rule. This includes concrete stacks such as:
        WriterT Log (RWST Env W S IO)
        RWST Env W S (WriterT Log IO)

    It also includes explicit specialization:
        type Stack m a = WriterT Log m a
        foo :: Stack (RWS Env W S) ()

    or the reverse:
        type Stack m a = RWST Env W S m a
        foo :: Stack (Writer Log) ()
    
    Because RWS/RWST intrinsically combines Reader, Writer, and State effects, actual RWS/RWST usage may also establish with_reader=true and with_state=true when it is directly combined with the Writer-related computation.
    Do not mark with_rws=true merely because Reader, Writer, and State capabilities happen to appear separately in the same file. The Writer-related computation must be directly combined with an actual RWS/RWST computation or abstraction.

You are allowed to read other files if it would help make a categorization certain. Write which extra files you explored in the comment column.

Return only a valid JSON object with the structure described earlier. No prose, no markdown, no code fences, no explanation.















