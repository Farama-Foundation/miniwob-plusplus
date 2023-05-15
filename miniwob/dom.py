"""Encapsulation of the DOM element tree."""
import re
from typing import Any, Collection, Dict, Optional, Sequence, Tuple, Union


class DOMElement:
    """Encapsulate the DOM element."""

    def __init__(self, raw_dom: Dict[str, Any], parent: Optional["DOMElement"] = None):
        """Create a new DOMElement based on the data from getDOMInfo in JavaScript.

        Args:
            raw_dom: A dict with values from getDOMInfo in JavaScript.
            parent: the parent DOMElement, or None
        """
        self._parent = parent
        self._tag = raw_dom["tag"].lower()
        self._left = raw_dom["left"]
        self._top = raw_dom["top"]
        self._width = raw_dom["width"]
        self._height = raw_dom["height"]
        self._ref = raw_dom["ref"]
        if "text" in raw_dom:
            self._text = str(raw_dom["text"])
        else:
            self._text = None
        self._value = raw_dom.get("value")
        self._id = raw_dom.get("id", "")
        classes = raw_dom.get("classes", "")
        if isinstance(classes, dict):
            classes = "SVG_CLASS"
        self._classes = classes
        self._bg_color = self._rgba_str_to_floats(raw_dom.get("bgColor"))
        self._fg_color = self._rgba_str_to_floats(raw_dom.get("fgColor"))
        self._focused = raw_dom.get("focused", False)
        self._tampered = raw_dom.get("tampered", False)
        self._targeted = raw_dom.get("recordingTarget", False)
        # Recurse on the children
        self._children = []
        for raw_child in raw_dom["children"]:
            self._children.append(DOMElement(raw_child, parent=self))
        # Fix a bug where sometimes children are created even though all children are <t>
        # (which will incorrectly make this element a non-leaf and thus unclickable)
        if self._children and all(child.tag == "t" for child in self._children):
            self._text = " ".join(child.text for child in self._children)
            self._children = []

    def __eq__(self, other: Any) -> bool:
        """Check if `self` and `other` refer to the same element.

        The reference ID is used for comparison. Elements are considered the same
        even when their attributes change (e.g., the position or text changes).
        """
        if not isinstance(other, DOMElement):
            return False
        return self.ref == other.ref

    def __ne__(self, other: Any) -> bool:
        """Check if `self` and `other` do not refer to the same element."""
        return not self.__eq__(other)

    @property
    def tag(self) -> str:
        """Return the lowercased tag name.

        For <input> tag, also append the input type (e.g., "input_checkbox").
        For Text node, the tag is "t".
        """
        return self._tag

    @property
    def left(self) -> float:
        """Return the left coordinate."""
        return self._left

    @property
    def top(self) -> float:
        """Return the top coordinate."""
        return self._top

    @property
    def width(self) -> float:
        """Return the width of the element."""
        return self._width

    @property
    def height(self) -> float:
        """Return the height of the element."""
        return self._height

    @property
    def right(self) -> float:
        """Return the right coordinate (left + width)."""
        return self._left + self._width

    @property
    def bottom(self) -> float:
        """Return the bottom coordinate (top + height)."""
        return self._top + self._height

    @property
    def ref(self) -> int:
        """Return the reference index.

        The ref is posive for normal elements and negative for text nodes.
        - Within the same episode, the ref of a DOM element remains the same
        - Exception: text nodes get a different ref at every time step
        - Ref number restarts at the beginning of each episode
        """
        return self._ref

    @property
    def text(self) -> Optional[str]:
        """Return the text content of the element.

        For non-leaf nodes, return None.
        """
        return self._text

    @property
    def value(self) -> Union[None, bool, str]:
        """Return the value of an input element, and None otherwise.

        - For checkbox and radio, return whether the element is selected (bool).
        - Otherwise, return the text inside the input.
        """
        return self._value

    @property
    def id(self) -> str:
        """Return the DOM id attribute, or an empty string."""
        return self._id

    @property
    def classes(self) -> str:
        """Return the DOM class attribute, or an empty string.

        Multiple classes are separated by spaces.
        """
        return self._classes

    @property
    def bg_color(self) -> Tuple[float, float, float, float]:
        """Return the background color as RGBA with value range 0.0 to 1.0."""
        return self._bg_color

    @property
    def fg_color(self) -> Tuple[float, float, float, float]:
        """Return the foreground color as RGBA with value range 0.0 to 1.0."""
        return self._fg_color

    @property
    def focused(self) -> bool:
        """Return whether the element is being focused on."""
        return self._focused

    @property
    def tampered(self) -> bool:
        """Return whether the element has been clicked on in this episode."""
        return self._tampered

    @property
    def targeted(self) -> bool:
        """In a recorded demonstration, return whether the element is an event target."""
        return self._targeted

    @property
    def is_leaf(self) -> bool:
        """Return whether this is a leaf element."""
        return self._text is not None

    @property
    def children(self) -> Sequence["DOMElement"]:
        """Return the list of children."""
        return self._children

    @property
    def subtree_elements(self) -> Collection["DOMElement"]:
        """Return the list of elements in the subtree, including self."""
        elements = [self]
        for child in self.children:
            elements += child.subtree_elements
        return elements

    @property
    def parent(self) -> Optional["DOMElement"]:
        """Return the parent, or None if the element is the root."""
        return self._parent

    @property
    def ancestor_path(self) -> Sequence["DOMElement"]:
        """Returns the path from root to self in a list, starting with root."""
        path = []
        curr = self
        while curr.parent:
            path.append(curr)
            curr = curr.parent
        return list(reversed(path))

    @property
    def depth(self) -> int:
        """Depth in the DOM tree (root is 1)."""
        return len(self.ancestor_path)

    def __str__(self) -> str:
        """Return the string representation."""
        if self.text:
            text = self.text
            text = text[:20] + "..." if len(text) > 20 else text
            text_str = f" text={repr(text)}"
        else:
            text_str = ""

        value_str = f" value={self.value}" if self.value is not None else ""
        classes_str = f" classes=[{self.classes}]"
        num_children = len(self.children)
        children_str = f" children={num_children}" if num_children != 0 else ""

        return "[{ref}] {tag} @ ({left}, {top}){text}{value}{classes}{children}".format(
            ref=self.ref,
            tag=self.tag,
            left=round(self.left, 2),
            top=round(self.top, 2),
            text=text_str,
            value=value_str,
            classes=classes_str,
            children=children_str,
        )

    __repr__ = __str__

    def visualize(self, join: bool = True) -> Union[str, Sequence[str]]:
        """Return a string visualizing the tree structure.

        Args:
            join: Whether to join the output lines with newlines.

        Returns:
            a list of string if join is True; a single string otherwise.
        """
        lines = []
        lines.append(f"- {self}")
        for i, child in enumerate(self.children):
            if isinstance(child, str):
                child = child[:20] + "..." if len(child) > 20 else child
                lines.append(f'  |- "{child}"')
            else:
                for j, line in enumerate(child.visualize(join=False)):
                    prefix = "   " if (i == len(self.children) - 1 and j) else "  |"
                    lines.append(prefix + line)
        return "\n".join(lines) if join else lines

    def lca(self, other: "DOMElement") -> "DOMElement":
        """Returns the least common ancestor of two DOMElement.

        The returned node is the node with greatest depth that is an ancestor
        of both `self` and `other`.
        """
        # One is kth deg grandparent of other
        if self in other.ancestor_path:
            return self
        elif other in self.ancestor_path:
            return other

        # Find the first spot at which the ancestor paths diverge
        for i, (self_ancestor, other_ancestor) in enumerate(
            zip(self.ancestor_path, other.ancestor_path)
        ):
            if self_ancestor != other_ancestor:
                return self.ancestor_path[i - 1]

        raise ValueError(
            (
                "{} is not in the same DOM tree as {}\n\nself tree: {}\n\n"
                "other tree: {}"
            ).format(self, other, self.visualize(), other.visualize())
        )

    def diff(self, other_dom: "DOMElement") -> Collection["DOMElement"]:
        """Compute the diffs with another subtree.

        Traverses the two DOM trees in the same order and returns all the
        elements that differ between the two in any of the following ways:
            - ref
            - text
            - tampered
            - value
            - left, top, width, height
            - classes
            - tag
            - fg_color, bg_color
            - is_leaf

        If two DOMElements have same ref but differ on properties, only ONE
        of them is added to the list, otherwise, both.

        Elements that do not exist in the other tree count as different.

        The operation is ordered: it compares the first child against first child,
        second child against second, and so on.

        Args:
            other_dom: Root of the tree to compare.

        Returns:
            The elements that differ.
        """

        def element_diff(first, second, diff_list):
            """Diffs two DOMElements, and adds them to list diff_list if they differ."""
            # Base cases
            if second is None:
                diff_list.append(first)
                for child in first.children:
                    element_diff(child, None, diff_list)
                return
            elif first is None:
                diff_list.append(second)
                for child in second.children:
                    element_diff(child, None, diff_list)
                return

            if first.ref != second.ref:
                diff_list.append(first)
                diff_list.append(second)
            else:
                if (
                    first.text != second.text
                    or first.tampered != second.tampered
                    # or first.focused != second.focused
                    or first.value != second.value
                    # or first.left != second.left
                    # or first.top != second.top
                    or first.width != second.width
                    or first.height != second.height
                    or first.classes != second.classes
                    or first.tag != second.tag
                    or first.fg_color != second.fg_color
                    or first.bg_color != second.bg_color
                    or first.is_leaf != second.is_leaf
                ):
                    diff_list.append(first)

            # Pad the children with None and diff them
            first_children = list(first.children)  # Make copy to not trash old
            second_children = list(second.children)
            if len(first_children) < len(second_children):
                first_children += [None] * (len(second_children) - len(first_children))
            elif len(first_children) > len(second_children):
                second_children += [None] * (len(first_children) - len(second_children))
            for first_child, second_child in zip(first_children, second_children):
                element_diff(first_child, second_child, diff_list)

        different_elements = []
        element_diff(self, other_dom, different_elements)
        return different_elements

    def _rgba_str_to_floats(
        self, rgba: Optional[str]
    ) -> Tuple[float, float, float, float]:
        """Convert the color string into normalized RGBA values.

        Takes a string of the form rgb(?, ?, ?) or rgba(?, ?, ?, ?)
        and extracts the rgba values normalized between 0 and 1.

        NOTE: If rgba is None, returns white (1.0, 1.0, 1.0, 1.0).
        NOTE: If only rgb is passed, assumes a = 100.
        """
        if rgba is None:  # Assume is white
            return 1.0, 1.0, 1.0, 1.0

        if "rgba" in rgba:
            m = re.search(r"rgba\(([0-9.]+), ([0-9.]+), ([0-9.]+), ([0-9.]+)\)", rgba)
            if not m:
                raise ValueError(f"Invalid color string: {rgba}")
            a = float(m.group(4))
        else:
            m = re.search(r"rgb\(([0-9.]+), ([0-9.]+), ([0-9.]+)\)", rgba)
            if not m:
                raise ValueError(f"Invalid color string: {rgba}")
            a = 1.0
        return (
            float(m.group(1)) / 255,
            float(m.group(2)) / 255,
            float(m.group(3)) / 255,
            a,
        )
