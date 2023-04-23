from types import FunctionType

from pinject.injection_contexts import InjectionContextFactory
from pinject.object_graph import ObjectGraph
from pinject.object_providers import ObjectProvider


def set_service_graph(object_graph: ObjectGraph):
    inject_service.object_graph = object_graph


def inject_service():
    """Flask RESTFul injector"""

    def wrapper(init_func: FunctionType):
        def decorated(*args, **kwargs):
            object_graph: ObjectGraph = inject_service.object_graph
            object_provider: ObjectProvider = getattr(object_graph, "_obj_provider")
            injection_context_factory: InjectionContextFactory = getattr(
                object_graph, "_injection_context_factory"
            )
            return object_provider.call_with_injection(
                init_func, injection_context_factory.new(init_func), args, kwargs
            )

        return decorated

    return wrapper


inject_service.object_graph = None
