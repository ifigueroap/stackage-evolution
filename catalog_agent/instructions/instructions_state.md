You are categorizing Haskell source code from Stackage packages that imports at least one of the following modules:
Control.Monad.State
Control.Monad.State.Class
Control.Monad.State.Lazy
Control.Monad.State.Strict
Those are the State modules in scope and State-related usage may be attributable to any of those modules. The import flags are independent. If multiple State modules are imported, mark every applicable flag.
Focus only on the usage attributable to those State imports. Consider a State use whenever an API symbol listed in the synopsis appears in the code and is attributable to one of those imports, provided that the symbol is not hidden by the import or redefined locally. Qualified and aliased uses also count.

Use only source-supported findings. Do not infer hidden types. You may inspect other files from the package when necessary to categorize the file accurately. Inspect only files that are relevant and likely to resolve uncertainty about the categorization.

This is the combined State API synopsis relevant for these modules:



class Monad m => MonadState s (m :: Type -> Type) | m -> s where
    get :: m s
    put :: s -> m ()
    state :: (s -> (a, s)) -> m a

modify :: MonadState s m => (s -> s) -> m ()
modify' :: MonadState s m => (s -> s) -> m ()
gets :: MonadState s m => (s -> a) -> m a

type State s = StateT s Identity
runState :: State s a -> s -> (a, s)
evalState :: State s a -> s -> a
execState :: State s a -> s -> s
mapState :: ((a, s) -> (b, s)) -> State s a -> State s b
withState :: (s -> s) -> State s a -> State s a

newtype StateT s (m :: Type -> Type) a = StateT (s -> m (a, s))
runStateT :: StateT s m a -> s -> m (a, s)
evalStateT :: Monad m => StateT s m a -> s -> m a
execStateT :: Monad m => StateT s m a -> s -> m s
mapStateT :: (m (a, s) -> n (b, s)) -> StateT s m a -> StateT s n b
withStateT :: (s -> s) -> StateT s m a -> StateT s m a

module Control.Monad.Trans


The Strict and Lazy modules expose overlapping State APIs with different evaluation behavior. Count a syntactic API occurrence once when it is attributable to one of the imported State modules. Do not multiply the count merely because more than one in-scope State module could export the same symbol.

Not every State module in scope necessarily exports every API symbol listed in this combined synopsis. Count an API occurrence only when the symbol is actually attributable to the State module imported by the file.

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
"api_usage": {
"MonadState": 1,
"state": 0,
"get": 1,
"put": 0,
"modify": 0,
"modify'": 0,
"gets": 0,
"State": 0,
"runState": 0,
"evalState": 0,
"execState": 0,
"mapState": 0,
"withState": 0,
"StateT": 1,
"runStateT": 0,
"evalStateT": 0,
"execStateT": 0,
"mapStateT": 0,
"withStateT": 0
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
"constraint_only": false,
"not_used": false,
"with_exceptions": false,
"with_io": false,
"with_writer": false,
"with_reader": false,
"with_parser": false,
"with_rws": false,
"re_export": false
},
"need_review": true
}

Where, "package_id", "module" and "file_path" are given to you.
"comment" Its an optional string with a brief comment about the module. Only use when explaining "need_review", noting unusual usage, suggesting a new category and reporting ambiguous use cases or difficulty in finding a fitting category. If you inspect another file, it should also be noted in the comment. Otherwise just "".

"explicit_import" is a boolean that indicates whether at least one State import uses an explicit import list. The State imports considered are the State modules in scope. This property is independent of whether the import is qualified.

Set explicit_import=true when at least one of these State modules specifies imported names in parentheses.

Examples:
    import Control.Monad.State (get, put)
    import qualified Control.Monad.State.Strict as S (StateT, modify')
    import Control.Monad.State.Class (MonadState, gets)

In all of these cases, explicit_import=true.

Set explicit_import=false when none of the State imports uses an explicit import list.

Examples:
    import Control.Monad.State
    import Control.Monad.State.Class
    import Control.Monad.State.Lazy
    import qualified Control.Monad.State.Strict as S

If multiple State variants are imported, explicit_import=true if at least one of them uses an explicit import list.

"qualified_import" is a boolean that indicates whether at least one State import uses the qualified keyword. The State imports considered are the State modules in scope. This property is independent of whether an explicit import list is present.

Set qualified_import=true when at least one of these State modules is imported qualified.

Examples:
    import qualified Control.Monad.State
    import qualified Control.Monad.State.Class as SC
    import qualified Control.Monad.State.Lazy as SL
    import qualified Control.Monad.State.Strict as SS (get, StateT)

In all of these cases, qualified_import=true.

Set qualified_import=false when all State imports are unqualified.

Examples:
    import Control.Monad.State.Class
    import Control.Monad.State.Strict (get)

If multiple State variants are imported, qualified_import=true if at least one of them is qualified.

"strict_import" is a boolean that indicates whether Control.Monad.State.Strict is imported. Set strict_import=true if Control.Monad.State.Strict appears in at least one import declaration, regardless of whether that import is qualified or uses an explicit import list.

Examples:
    import Control.Monad.State.Strict
    import Control.Monad.State.Strict (get, modify')
    import qualified Control.Monad.State.Strict as S

In all of these cases, strict_import=true. Otherwise, set strict_import=false.

"lazy_import" is a boolean that indicates whether Control.Monad.State.Lazy is imported. Set lazy_import=true if Control.Monad.State.Lazy appears in at least one import declaration, regardless of whether that import is qualified or uses an explicit import list.

Examples:
    import Control.Monad.State.Lazy
    import Control.Monad.State.Lazy (get, StateT)
    import qualified Control.Monad.State.Lazy as S

In all of these cases, lazy_import=true. Otherwise, set lazy_import=false.

These import flags are independent. More than one may be true at the same time.
For example:
    import Control.Monad.State.Strict (get)
    import qualified Control.Monad.State.Lazy as L
gives:
    explicit_import = true
    qualified_import = true
    strict_import = true
    lazy_import = true

"class_import": Set class_import=true if Control.Monad.State.Class is imported at least once. Otherwise, set class_import=false.

Example:
    import Control.Monad.State.Class
or:
    import qualified Control.Monad.State.Class as SC

Both give class_import=true.

Importing Control.Monad.State, Control.Monad.State.Lazy, or Control.Monad.State.Strict does not by itself make class_import=true, even though those modules may re-export MonadState operations.

"need_review" is a boolean, true if you consider that no category fits properly, or if you lack context or information to properly categorize, or if simply there is something strange in the file. Leaving a brief comment about it in the "comment".

"api_usage" contains an int count for every listed API symbol attributable to the State-related imports stated at the beginning of these instructions. Should only count the occurrences as they come from the import, for example, redefining `get` in an unrelated way does not count; although defining `get`, `put`, or `state` as methods of a MonadState instance does count. Declaration heads, instance heads, method definitions, method usages, deriving clauses and type signatures are counted as occurrences. Occurrences in module export lists also count. Do not count the import or explicit import occurrences. Do not count commented or string occurrences. A symbol is counted only when syntactically attributable to any of the State modules in scope, either through an unqualified import binding or through a qualified/aliased import of any of the State modules in scope.

For example:



    deriving (MonadState S)



counts as one occurrence of MonadState. It does not count implicit occurrences of get, put or state, since those symbols do not syntactically appear.
Count every attributable syntactic occurrence in code, including repeated identical local definitions in different scopes. Do not deduplicate occurrences merely because the surrounding code is structurally duplicated.
When the same unqualified API name could have been exported by multiple State modules imported into the file, count the source occurrence once, not once per possible exporting module.
When counting repeated API uses, inspect the whole file rather than one representative definition; identical or near-identical local blocks in different scopes each contribute their own occurrences.

"categories" these are independent boolean properties. A file might satisfy multiple categories simultaneously. "categories" contains the categories in which the usage of State monad falls into for this file. A property or category is marked true if it fits the criteria for said category, which are explained below. Also, categories are not necessarily mutually exclusive and a single file may contain several different uses, resulting in multiple categories being present.

1. lifting:
   Mark lifting=true when a transformer or wrapper other than StateT is given MonadState capability by explicitly forwarding one or more State operations to an underlying monad that already provides MonadState. For example:
        instance MonadState s m => MonadState s (MyT m) where
            get = lift get
            put = lift . put
            state = lift . state

   Here the MyT transformer is receiving State capability from m, so lifting=true.

   Do not mark it when StateT itself is the transformer layer being implemented; that belongs to lifting_t.

   Also do not mark lifting=true merely because a newtype or application wrapper around StateT derives or exposes the MonadState capability supplied by that StateT. For example:
        newtype AppT m a = AppT { unAppT :: StateT AppState m a }
            deriving (Monad, MonadState AppState)
   
   This alone does not establish lifting=true; State is the capability of the wrapped StateT rather than a capability being forwarded from an underlying monad through another transformer.

2. lifting_t:
   Mark lifting_t=true when StateT itself is the transformer layer whose generic implementation or transformer behavior is being defined. This includes implementing MonadState for StateT, or giving a polymorphic StateT another capability by forwarding operations to its underlying monad:

        instance MyMonadClass m => MyMonadClass (StateT s m) where
            myMethod = lift myMethod
            myOtherMethod = mapStateT myOtherMethod


   Here StateT is the transformer receiving the capability, so lifting_t=true.

   If the file defines or implements MonadState for StateT, that also counts as lifting_t=true:
        instance Monad m => MonadState s (StateT s m) where
            get = StateT $ \s -> return (s, s)
            put s = StateT $ \_ -> return ((), s)

   Do not mark direct_use_inner, direct_use_middle, or direct_use_outer merely because StateT appears in such an instance. Those categories require an actual StateT computation used as part of the program's computation stack.

   An arbitrary concrete domain-class instance whose head happens to contain a concrete StateT stack is not automatically lifting_t. For example:
        instance ByteSource (StateT Cache IO) where
            readByte = ...
   

   does not establish lifting_t merely because StateT occurs in the instance head. lifting_t requires generic StateT implementation/transformer behavior, such as forwarding a capability through `StateT s m` from the underlying `m`.

For direct_use_inner, direct_use_middle, and direct_use_outer, classify the position of an actual StateT computation relative to other transformer layers. An actual StateT computation is one where the ordinary computation being classified is written directly in StateT, or in a transparent type synonym that expands to StateT. The monad underneath StateT does not have to be fully concrete; for example, `StateT S m` can still be an actual StateT computation when it is used as the program's State transformer stack. A distinct newtype, data type, or domain-specific wrapper around StateT does not by itself make ordinary computations in that wrapper direct StateT uses; State operations used through such a wrapper's MonadState instance belong to concrete_interface_use. Generic instances whose purpose is to define, lift, or forward behavior through StateT are not direct uses.

A StateT occurrence in an instance head does not by itself establish a direct-use category. Mark a direct-use category only when StateT is being used directly as the ordinary computation stack, or through a transparent type synonym, not merely when an instance or capability is being implemented for StateT or when StateT is hidden inside a distinct wrapper.

When the same file contains distinct StateT computations in different positions, more than one direct-use positional category may be true. Likewise, expanding a concrete specialization of a polymorphic StateT type synonym may reveal an additional positional category for that specialized computation.

For these positional categories, a base monad means a monad underneath StateT that is not itself a transformer layer. It is not restricted to IO or Identity; for example, `[]` may be the base monad in `StateT S []`.

3. direct_use_pure:
   Mark direct_use_pure=true when an ordinary computation is written directly in State, `StateT s Identity`, or a transparent type synonym that expands to one of those, and has no effects other than State itself. So we would see things like `State s a` or `StateT s Identity a`. A simple example would be:

        increment :: State Int ()
        increment = modify (+1)

   A distinct newtype or domain-specific wrapper around State does not establish direct_use_pure merely because its implementation contains State. State operations used through that wrapper's MonadState instance belong to concrete_interface_use.

   Do not mark direct_use_inner, direct_use_middle, or direct_use_outer solely because of a pure State or `StateT s Identity` computation.

4. direct_use_inner:
   Mark direct_use_inner=true when an actual StateT computation has at least one transformer layer above it, but no transformer layer below it; only a base monad is underneath StateT. So things like `ReaderT Env (StateT S IO)` make direct_use_inner=true. An example:
        type MyStack = ReaderT Config (StateT Int IO)
        increment :: MyStack ()
        increment = lift (modify (+1))

   Here another transformer wraps StateT, while only the base monad is below StateT.

5. direct_use_middle:
   Mark direct_use_middle=true when an actual StateT computation has at least one transformer layer above it and at least one transformer layer below it. For example:
        type MyStack = ReaderT Config (StateT Int (ExceptT String IO))
        increment :: MyStack ()
        increment = lift (modify (+1))
   
   ReaderT is above StateT, and ExceptT is below it, therefore direct_use_middle=true. Note that we use the word "middle" loosely, as we dont care if there are more layers above or below, only that there is at least one above and one below.

6. direct_use_outer:
   Mark direct_use_outer=true when an actual StateT computation has no transformer layer above StateT. The monad underneath StateT may be a base monad or another transformer stack. Like so:
        StateT S IO
        StateT S []
        StateT S (ReaderT Env IO)
        StateT S (ExceptT Error IO)

   In all four cases, StateT is the outermost transformer layer.

   An example of direct_use_outer=true would be:
        type MyStack = StateT AppState IO
        runTask :: MyStack ()
        runTask = do
            modify updateState
            liftIO performIO

   A StateT directly over a base monad and with no transformer layer above it, such as StateT S IO, then is outer, not inner. A polymorphic StateT computation such as:
        type MyStack m = StateT AppState m
   can also establish direct_use_outer=true when it is genuinely used as a computation stack, because StateT is the outermost transformer even though the monad underneath it remains abstract.

In polymorphic_interface_use and concrete_interface_use, “interface” refers to the corresponding effect typeclass, in this case MonadState.

7. polymorphic_interface_use:
   Mark polymorphic_interface_use=true when an ordinary function or computation runs in a genuinely abstract monad constrained by MonadState, and its implementation actually uses State operations such as state, get, put, modify, modify' or gets.
   Example:
        increment :: MonadState Int m => m ()
        increment = modify (+1)
   Here the concrete monad is not fixed; it is chosen by the caller, and the function actually uses State functionality, so polymorphic_interface_use=true.

   A type synonym or newtype that expands to a concrete State/StateT stack does not count as polymorphic use merely because the underlying implementation is hidden.

   Likewise, a computation whose outer monad constructor is a specific wrapper such as `AppT m` does not count as polymorphic_interface_use merely because `m` remains abstract. If State operations are dispatched through the MonadState instance of that specific wrapper, that belongs to concrete_interface_use.

   Do not mark polymorphic_interface_use=true for MonadState instance implementations whose purpose is to lift or forward State behavior through a transformer or wrapper. Those belong to the lifting or lifting_t categories.

   State operations used inside an instance method of some unrelated class still count as polymorphic_interface_use when the method runs in an abstract MonadState-constrained monad. Only MonadState instance implementations whose purpose is forwarding/lifting are excluded.

8. concrete_interface_use:
   Set concrete_interface_use=true when State operations such as state, get, put, modify, modify' or gets are used in a specific monad type that has a MonadState instance, but the ordinary computation is not itself State or StateT.

   This category is for specific monad constructors or wrappers that provide State functionality through a MonadState instance. The monad does not need to have every type parameter fixed; a type such as `AppT m` can count as a specific monad type when State operations are dispatched through the MonadState instance of `AppT m`.
   Example:
        newtype MyMonad a = MyMonad ...
        instance MonadState AppState MyMonad where
            get = ...
            put = ...

        foo :: MyMonad AppState
        foo = get
   Here foo uses State functionality in the concrete monad MyMonad, therefore concrete_interface_use=true.

   A parameterized wrapper can also count. For example:
        newtype AppT m a = AppT ...
        instance MonadState s m => MonadState s (AppT m) where
            get = lift get
            put = lift . put

        foo :: MonadState S m => AppT m S
        foo = get
   Here foo uses State through the MonadState instance of the specific wrapper `AppT m`, therefore concrete_interface_use=true, even though the underlying `m` remains polymorphic.

   Defining the MonadState instance itself does not by itself establish concrete_interface_use; there must be an ordinary computation using the interface in that specific monad.

   The MonadState instance may be defined in another module. If necessary, inspect the relevant definition to establish that the specific monad has a MonadState instance.

   Do not mark direct_use_pure, direct_use_inner, direct_use_middle or direct_use_outer merely because this specific monad is internally implemented using State or StateT. Those direct-use categories are reserved for ordinary computations written directly in State/StateT, or in transparent type synonyms that expand to State/StateT.

   For example:
        newtype App a = App (StateT AppState IO a)
            deriving (Functor, Applicative, Monad, MonadState AppState)

        foo :: App AppState
        foo = get
   Here concrete_interface_use=true, while direct_use_outer=false. Although App is implemented using StateT AppState IO, the ordinary computation foo is written against the distinct concrete type App and accesses State through App's MonadState instance.

   Likewise:
        newtype Update s a = Update (State s a)
            deriving (Functor, Applicative, Monad, MonadState s)

        foo :: Update S S
        foo = get
   gives concrete_interface_use=true and direct_use_pure=false, because foo is written against the distinct wrapper Update rather than directly against State.

   Do not mark concrete_interface_use=true when the ordinary computation itself is State or StateT. Those uses belong to the appropriate direct_use_* category instead.

   Do not mark concrete_interface_use=true merely because a specific monad has a MonadState instance. State operations must actually be used in an ordinary computation through that monad's MonadState interface.

   In particular, distinguish between using the wrapper's MonadState instance and explicitly constructing the wrapper around an operation in a contained StateT. For example:
        newtype AppT m a = AppT (StateT InnerState m a)

        instance MonadState s m => MonadState s (AppT m) where
            get = lift get
            put = lift . put

        readInner :: AppT m InnerState
        readInner = AppT get

   The `get` in `AppT get` runs directly in the contained `StateT InnerState m`; it is not dispatched through the forwarding `MonadState s (AppT m)` instance. Therefore this use does not by itself establish concrete_interface_use for AppT. Because the contained computation is explicitly written as StateT, that StateT use may establish the appropriate direct_use_* category.

9. constraint_only:
   Mark constraint_only=true when at least one State-related use has MonadState only as a type-level requirement, such as in a function signature, class constraint, or data/type declaration, but that particular use does not actually execute State operations and does not use a concrete State or StateT computation.

   Example:
        foo :: MonadState Int m => Int -> m Int
        foo x = pure (x + 1)
    

   Here MonadState is required by the type signature, but no State operation such as state, get, put, modify, modify' or gets is used by foo, so constraint_only=true.

   constraint_only is existential: it may be true even if other State-related uses elsewhere in the same file belong to other categories.

   For example:
        foo :: MonadState Int m => Int -> m Int
        foo x = pure (x + 1)

        bar :: MonadState Int m => m ()
        bar = modify (+1)
    

   gives both constraint_only=true and polymorphic_interface_use=true.

   Do not mark a particular use as constraint_only if that same computation:

   * actually executes State operations,
   * uses concrete State/StateT computations or runners,
   * defines a MonadState instance,
   * or re-exports State API.

   Defining a MonadState instance or re-exporting MonadState does not by itself establish constraint_only.

   For abstract MonadState-constrained code:
   if State operations are actually executed -> polymorphic_interface_use
   if MonadState is only required at the type/API level -> constraint_only

10. not_used:
    Mark not_used=true when the file imports any of the State modules in scope, but contains no attributable use of any State API symbol from that import.

    This means there is no use of MonadState, state, get, put, modify, modify', gets, State, runState, evalState, execState, mapState, withState, StateT, runStateT, evalStateT, execStateT, mapStateT or withStateT. In this case, all api_usage counts should be 0.

    Do not count:

    * the import declaration itself,
    * occurrences in comments or string literals,
    * unrelated local definitions that reuse names such as state, get, put or modify,
    * record fields or other local names that shadow an imported State API name,
    * names that are hidden by the import,
    * qualified Template Haskell names that do not refer to the imported State API.

    not_used is mutually exclusive with every other State-usage category, including re_export.
    example of re_export=true and not_used=false:
        module Foo (get) where
        import Control.Monad.State (get)
        ... -- file continues without further use of the State API.
    Then api_usage counts are all 0 except for get=1.

11. re_export:
    Mark re_export=true when the module exports any symbol that comes from any of the State modules in scope, either by re-exporting the whole imported module or by exporting individual imported State API symbols.

    Example:
        module Foo (get) where
        import Control.Monad.State (get)
    In these cases, re_export=true. Export-list occurrences of individual State API symbols also count toward api_usage.
    A whole-module re-export such as:
        module Foo (module Control.Monad.State.Strict) where
        import Control.Monad.State.Strict
    gives re_export=true, but the module name itself is not an occurrence of each individual API symbol. Do not increment every api_usage field merely because the entire module is re-exported.

    Do not mark re_export=true merely because a locally defined function with the same name as a State API symbol is exported; the exported symbol must actually come from the State import.

General rule for with_* categories: A with_* category is true when the State-related computation directly contains, executes, interprets, or is structurally combined with the corresponding effect or abstraction (* can be io, writer, reader, parser, rws or exceptions; they will be explained shortly after this section). A combination can be established by:

a. Structural combination:
    The corresponding * effect is part of the same monad stack that contains State or StateT. For example:
        type App = StateT AppState (ReaderT Env IO)

    This directly establishes with_io=true.

    Structural presence of Reader or Writer alone does not establish with_reader or with_writer. Those two categories additionally require actual Reader or Writer API usage attributable to the relevant imports and combined with the State-related computation, as described in their respective sections.

    The important point is that the effect is part of the same stack, not merely somewhere else in the module.

    If the base monad is a project-defined alias or newtype and its relevant capabilities cannot be determined from the current file, inspect its definition when necessary. Expand it far enough to establish source-supported capabilities of the concrete State computation. For example:

        type App = StateT AppState CustomM

    If inspection establishes that CustomM provides MonadError Error and IO as capabilities of this concrete computation, then with_exceptions=true and with_io=true. If it provides Reader or Writer capability, the additional usage requirement for with_reader or with_writer still applies. Do not stop merely because the base monad is a custom abstraction.

    Do not equate an arbitrary project-specific typeclass whose name contains "State" with the State effect. For example, a read-only class such as `ReadTCState` does not by itself establish State/MonadState semantics. Require source-supported mutable State capability or an actual State/StateT/MonadState computation when making State-specific conclusions.

b. Explicit specialization:
    A polymorphic stack is explicitly instantiated with another effect, making the resulting computation involve State/StateT and another effect *.
    Example:
        type MyStack m a = StateT AppState m a
        foo :: MyStack (Writer Log) ()

    Here the alias expands to a concrete State + Writer stack. This establishes the structural combination, but with_writer additionally requires actual attributable Writer API usage combined with that State-related computation.

    We could also have something like:

        type MyStack m a = ReaderT Env m a
        foo :: MyStack (State AppState) ()

    Where the alias expands to a concrete Reader + State stack. This establishes the structural combination, but with_reader additionally requires actual attributable Reader API usage combined with that State-related computation.

    Follow type aliases through concrete type arguments even when the specialization appears inside another type or API signature.

    For example:

        type Run m = ExceptT Error (StateT S m)
        makeContext :: Context (Run (Reader Env))

    establishes a State + Reader specialization if this specialized Run computation is genuinely part of the API/computation being defined or used. with_reader additionally requires actual attributable Reader API usage associated with that State-related computation.

    Such a concrete specialization can also affect StateT positional categories. For example, if a generic type contains `StateT S m` with no transformer below StateT, but a used specialization sets `m = ReaderT Env IO`, then the generic StateT computation may establish direct_use_outer while the specialized computation also establishes direct_use_outer. If there is a transformer above StateT, specialization may turn an inner StateT occurrence into a middle StateT occurrence. Evaluate each genuinely used concrete computation separately.


c. Shared polymorphic capability:
    The same abstract monad has both MonadState and * capability, and the implementation actually uses operations from both capabilities.
    Example:
        foo :: (MonadState S m, MonadIO m) => m ()
        foo = do
            modify update
            liftIO ...

    Therefore with_io=true.

    Merely having both constraints in the type signature is not sufficient. The function body must actually use State functionality and the corresponding capability.

    Effect usage may be direct, or through a called operation whose exposed type/signature explicitly requires the corresponding effect capability or whose API purpose explicitly performs that effect. Incidental implementation details hidden inside otherwise unrelated helpers do not count.

d. Nested effect execution:
    A with_* category may also be true when a computation running in a State-capable monad explicitly runs or interprets another effect inside that same computation, even if that effect is not structurally part of the State stack.

    Example:

        parser :: ExceptT Error m Int
        foo :: MonadState S m => m (Either Error Int)
        foo = do
            modify update
            runExceptT parser

    Then with_exceptions=true.

    Likewise:

        environment :: Reader Env Int
        foo :: MonadState S m => m Int
        foo = do
            modify update
            pure (runReader environment env)

    gives with_reader=true.

e. Polymorphic effect specialization:
    A with_* category is also true when a polymorphic computation that explicitly performs the corresponding effect is concretely instantiated with a State/StateT-containing monad, and that specialization is actually used, executed, or tested. Merely defining an unused compatible State-specialized value is not sufficient.

    Do not mark a with_* category merely because the corresponding module, typeclass, type, or function appears elsewhere in the file. The effect must be directly related to the State computation being categorized. Do not infer combinations from effects hidden inside imported helper functions. If the purpose/signature of an imported helper is necessary to determine whether it directly adapts, executes, parses, catches, or otherwise controls the State computation, inspect the relevant definition rather than guessing.

12. with_exceptions:
    Mark with_exceptions=true when State is directly combined with exception handling according to the general with_* rule. This includes stacks such as:
        StateT S (ExceptT Error IO)
        ExceptT Error (StateT S IO)
    
    It also includes polymorphic code where the same abstract monad actually uses both State and exception capabilities:
        foo :: (MonadState S m, MonadError Error m) => m ()
        foo = do
            modify update
            throwError err
    And it includes explicitly running or interpreting an exception computation as part of a State-related computation:
        computation :: ExceptT Error m Int
        foo :: MonadState S m => m (Either Error Int)
        foo = do
            modify update
            runExceptT computation
    Do not mark with_exceptions=true merely because exception-related types or functions appear elsewhere in the file and are unrelated to the State computation.

    Exception handling is semantic and is not restricted to Except/ExceptT or MonadError. It also includes exception APIs such as Control.Exception, MonadThrow, MonadCatch, MonadMask, throwM, catch, try, mask, finally, throwIO, catchIO, and equivalent project-specific abstractions.

    If a State computation is run inside such exception handling, or such exception handling is used to execute/control the State computation, with_exceptions=true.
    For example:
        foo :: StateT S IO a -> IO (Either SomeException (a, S))
        foo st = try (runStateT st initialState)
    gives with_exceptions=true.

    The combination is symmetric with respect to interpretation. It also counts when an exception-capable computation runs/interprets a State computation:
        foo :: MonadError Error m => StateT S Parser a -> m a
        foo st =
            case runParser (evalStateT st initialState) of
                Left err -> throwError err
                Right x -> pure x
    Here with_exceptions=true.

    If a generic exception test/computation is actually instantiated and executed with StateT, the combination counts. For example:
        testCatch :: MonadCatch m => MSpec m -> ...
        stateSpec :: MSpec (StateT S IO)
    If testCatch is actually run using stateSpec, then with_exceptions=true.

    If a State computation is executed by an interpreter/helper whose execution can throw or propagate exceptions, this counts as with_exceptions, even if the State operation itself is written in a separate helper or wrapper.

13. with_io:
    Mark with_io=true when State is directly combined with IO according to the general with_* rule. This includes stacks such as:
        StateT S IO
        ReaderT Env (StateT S IO)
        StateT S (ReaderT Env IO)
    It also includes polymorphic code where the same abstract monad actually uses both State and IO capabilities:
        foo :: (MonadState S m, MonadIO m) => m ()
        foo = do
            modify update
            liftIO performIO
    In this case, with_io=true because the computation actually uses both State functionality and IO functionality.

    Do not mark with_io=true merely because MonadIO appears in a constraint, or because IO-related code appears elsewhere in the file without being part of the State-related computation.

14. with_writer:
    Mark with_writer=true when State is directly combined with Writer according to the general with_* rule and the file presents actual Writer API usage attributable to a Writer import in conjunction with the State-related computation.

    Structural presence of Writer or WriterT in a State stack is not sufficient by itself. Likewise, the presence of MonadWriter as a capability is not sufficient unless Writer functionality is actually used. For example:
        foo :: (MonadState S m, MonadWriter Log m) => m ()
        foo = do
            modify update
            tell ["updated"]
    gives with_writer=true because the same computation actually uses both State and Writer functionality.
    Concrete stacks can also establish with_writer when Writer functionality is actually used:
        type Stack = StateT S (Writer Log)

        foo :: Stack ()
        foo = do
            modify update
            tell ["updated"]
    Likewise for the reverse stack:
    type Stack = WriterT Log (State S)
        foo :: Stack ()
        foo = do
            tell ["updated"]
            lift (modify update)
    Writer runners or other Writer API operations may also establish with_writer when they execute, interpret, or otherwise directly operate in conjunction with the State-related computation.

    Reader/Writer usage does not have to occur in the same function as every other State-related use in the file. If one function genuinely combines State and Writer, with_writer=true even if other State-related functions do not use Writer.

    Do not mark with_writer=true merely because MonadWriter, Writer, WriterT, tell, or related Writer code appears elsewhere in the file without being directly related to the State computation.

15. with_reader:
    Mark with_reader=true when State is directly combined with Reader according to the general with_* rule and the file presents actual Reader API usage attributable to a Reader import in conjunction with the State-related computation.

    Structural presence of Reader or ReaderT in a State stack is not sufficient by itself. Likewise, the presence of MonadReader as a capability is not sufficient unless Reader functionality is actually used. For example:
        foo :: (MonadState S m, MonadReader Env m) => m ()
        foo = do
            modify update
            env <- ask
            ...
 
    gives with_reader=true because the same computation actually uses both State and Reader functionality.

    Concrete stacks can also establish with_reader when Reader functionality is actually used:
        type Stack = StateT S (Reader Env)

        foo :: Stack ()
        foo = do
            modify update
            env <- ask
            ...
    Likewise for the reverse stack:
    type Stack = ReaderT Env (State S)
        foo :: Stack ()
        foo = do
            env <- ask
            lift (modify update)
    Reader runners or other Reader API operations may also establish with_reader when they execute, interpret, or otherwise directly operate in conjunction with the State-related computation.

    Reader/Writer usage does not have to occur in the same function as every other State-related use in the file. If one function genuinely combines State and Reader, with_reader=true even if other State-related functions do not use Reader.

    Do not mark with_reader=true merely because MonadReader, Reader, ReaderT, ask, local, asks, reader, or related Reader code appears elsewhere in the file without being directly related to the State computation.

16. with_parser:
    Mark with_parser=true when State is directly combined with a parser computation according to the general with_* rule. This includes State used to track or mutate parser/token-processing context while interpreting a parser AST or preprocessing parser tokens, even when the State computation itself is plain State/StateT rather than a parser transformer.
    This includes concrete stacks where a parser transformer and State are part of the same computation stack, for example:
        StateT S (ParsecT e input m)
        ParsecT e input (StateT S m)

    It also includes explicit specialization:
        type Stack m a = StateT S m a
        foo :: Stack (Parsec e input) Result 
    or the reverse:
        type ParserT m a = ParsecT e input m a
        foo :: ParserT (State S) Result
    It can also apply when a State-related computation explicitly runs or interprets a parser computation as part of its work:
        foo :: MonadState S m => Input -> m (Either ParseError Result)
        foo input = do
            modify update
            pure (parse parser "" input)

    Parser functionality is semantic and is not restricted to standard parser libraries. A State-based abstraction that is explicitly defined or used as a parser also counts.
    For example:
    --the Parser monad.
        type Parser a = StateT ParseState (Either ParseError) a
    If this abstraction is actually used by parsing operations and a parser runner, then with_parser=true.

    State-backed parser state, token-state machinery, or other project-specific State-based parsing infrastructure can also establish with_parser when the State computation is genuinely part of parsing behavior. Unlike with_reader and with_writer, this category does not require a particular standard parser API symbol to be imported and used.

    Likewise, a helper that directly transforms or adapts the State-related handler by parsing its input can establish with_parser when the parser is part of the execution path of that State computation. Inspect such a helper when necessary rather than inferring from its name alone.

    Do not mark with_parser=true merely because parser-related imports, parser types, or parsing functions occur elsewhere in the file without being directly related to the State computation.


17. with_rws:
    Mark with_rws=true when State is directly combined with an RWS computation according to the general with_* rule. This includes concrete stacks such as:
        StateT S (RWST Env W R IO)
        RWST Env W R (StateT S IO)
    It also includes explicit specialization:
        type Stack m a = StateT S m a
        foo :: Stack (RWS Env W R) ()
    or the reverse:
        type Stack m a = RWST Env W R m a
        foo :: Stack (State S) ()

    RWS/RWST intrinsically contains a State capability of its own. Therefore ordinary State operations used through the MonadState instance of a concrete RWS/RWST computation can establish concrete_interface_use and with_rws when that RWS/RWST computation is the State-related computation being classified.

    with_rws does not subsume with_reader or with_writer. Evaluate them independently.

    The fact that RWS/RWST structurally contains Reader and Writer does not by itself establish with_reader=true or with_writer=true. To mark with_reader=true, the file must present actual Reader API usage attributable to a Reader import in conjunction with a State-related computation. To mark with_writer=true, the file must present actual Writer API usage attributable to a Writer import in conjunction with a State-related computation.
    For example:
        foo :: RWS Env Log S ()
        foo = modify update
    may establish with_rws=true and concrete_interface_use=true, but does not by itself establish with_reader or with_writer.
    On the other hand:
        foo :: RWS Env Log S ()
        foo = do
            modify update
            env <- ask
            tell ["updated"]
    can establish with_rws=true, with_reader=true and with_writer=true, provided the Reader and Writer symbols are attributable to the corresponding imports.

    The Reader and Writer combinations do not need to occur in the same function. For example, if one State-related function uses Reader functionality and another State-related function uses Writer functionality, then both with_reader=true and with_writer=true.

    Do not mark with_rws=true merely because State, Reader, and Writer capabilities happen to appear separately in the same file. The State-related computation must be directly combined with an actual RWS/RWST computation or abstraction.

You are allowed to read other files if it would help make a categorization certain. Write which extra files you explored in the comment column.
This is a categorization task, not a general code review. Do not report bugs, security issues, style issues, vulnerabilities, or unrelated findings. Only inspect code as needed to determine the requested State usage fields and categories.
Return only a valid JSON object with the structure described earlier. No prose, no markdown, no code fences, no explanation.
