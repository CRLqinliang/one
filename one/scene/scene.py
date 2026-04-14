from one.scene.scene_object import SceneObject
from one.robots.base.mech_base import MechBase


def _walk_subtree(sobj):
    """Yield sobj and all its descendants in the scene-node tree, depth-first."""
    yield sobj
    for c in sobj.children:
        yield from _walk_subtree(c)


class Scene:

    def __init__(self):
        self.dirty = True  # shader group needs update
        self._sobjs = []
        self._lnks = []
        self._mecbas = []

    def __iter__(self):  # for rendering order
        for sobj in self._sobjs:
            yield from _walk_subtree(sobj)
        for lnk in self._lnks:
            yield from _walk_subtree(lnk)

    def add(self, entity):
        if isinstance(entity, SceneObject):
            if entity not in self._sobjs:
                self._sobjs.append(entity)
        elif isinstance(entity, MechBase):
            if entity not in self._mecbas:
                self._mecbas.append(entity)
                for lnk in entity.runtime_lnks:
                    if lnk not in self._lnks:
                        self._lnks.append(lnk)
        else:
            raise TypeError(f"Unsupported type: {type(entity)}")
        self.dirty = True

    def remove(self, entity):
        if isinstance(entity, SceneObject):
            if entity in self._sobjs:
                self._sobjs.remove(entity)
        elif isinstance(entity, MechBase):
            for lnk in entity.runtime_lnks:
                if lnk in self._lnks:
                    self._lnks.remove(lnk)
            if entity in self._mecbas:
                self._mecbas.remove(entity)
        self.dirty = True

    @property
    def sobjs(self):
        return tuple(self._sobjs)

    @property
    def lnks(self):
        return tuple(self._lnks)

    @property
    def mecbas(self):
        return tuple(self._mecbas)

    @property
    def visual_sobjs(self):
        return tuple(self._visual_sobjs)
