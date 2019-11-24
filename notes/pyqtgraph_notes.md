# Technical Research

## Basic concepts of the Qt GUI Framework (https://wiki.qt.io/Qt_for_Beginners)

To understand following code samples and concepts, it is important to understand
the most important concepts that the Qt framework is built on top of.

`QObject` as a base class for most Qt classes, that provides the parenting system
as well as signals and slot etc.

- Parenting System (inherited from `QObject`):
    - All items can be arranged in a hirarchical tree with child <-> parent references
    - Automatic destroying of children, if parents are destroyed
    - All children of a `QWidget` automatically appear in them

- Observer pattern for detecting and handling user interaction
  - Signal and Slot mechanism as a convenient implementation of this observer pattern
  - `Signal`: Emit messages that provide information about a state change
  - `Slot`: Functions that react on a state change
  - Signals are `connected` to Slots (`n:m`)
  - Signals can also be connected to signals -> Signals Relaying


## Graphics View Framework
- Graphics View Framework