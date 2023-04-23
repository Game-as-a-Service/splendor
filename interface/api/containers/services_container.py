from typing import Type, TypeVar

import pinject
from flask import Flask
from pinject.arg_binding_keys import ArgBindingKey
from pinject.arg_binding_keys import new as new_binding_key
from pinject.bindings import Binding, BindingMapping
from pinject.injection_contexts import InjectionContextFactory
from pinject.object_graph import ObjectGraph
from pinject.object_providers import ObjectProvider

from interface.api.containers.decorator import set_service_graph
from interface.api.containers.services_spec import BindingSpec, service_classes

T = TypeVar("T")


class ServicesContainer:
    app: Flask
    service_graph: ObjectGraph

    def __init__(self, app: Flask = None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        container = self.init_container(app)

        app.extensions = getattr(app, "extensions", {})
        app.extensions["container"] = container

    def init_container(self, app: Flask):
        self.service_graph = create_service_graph(app)
        return self

    def provide_instance(self, cls: Type[T]) -> T:
        return self.service_graph.provide(cls)

    def provide(self, name: str):
        return get_binding_instance_from_object_graph(self.service_graph, name)


def create_service_graph(app: Flask) -> ObjectGraph:
    binding_spec = BindingSpec(app)
    service_graph = pinject.new_object_graph(
        modules=None,
        binding_specs=[binding_spec],
        classes=service_classes,
    )
    set_service_graph(service_graph)
    return service_graph


def get_binding_instance_from_object_graph(object_graph: ObjectGraph, name: str):
    arg_binding_key: ArgBindingKey = new_binding_key(name)
    object_provider: ObjectProvider = getattr(object_graph, "_obj_provider")
    injection_context_factory: InjectionContextFactory = getattr(
        object_graph, "_injection_context_factory"
    )
    binding_mapping: BindingMapping = getattr(object_provider, "_binding_mapping")
    binding: Binding = binding_mapping.get(arg_binding_key.binding_key, "")
    return binding.proviser_fn(
        injection_context_factory.new(get_binding_instance_from_object_graph),
        object_provider,
        [],
        {},
    )
