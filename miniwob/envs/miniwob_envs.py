"""Environments for MiniWoB tasks as defined in Shi et al., 2017."""

from miniwob.environment import MiniWoBEnvironment


class BisectAngleEnv(MiniWoBEnvironment):
    """
    ## Description

    Find the line that bisects an angle evenly in two.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "bisect-angle"


class BookFlightEnv(MiniWoBEnvironment):
    """
    ## Description

    Search for flight results.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "book-flight"


class BookFlightNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [book-flight]

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "book-flight-nodelay"


class ChooseDateEnv(MiniWoBEnvironment):
    """
    ## Description

    Learn to operate a date picker tool.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "choose-date"


class ChooseDateEasyEnv(MiniWoBEnvironment):
    """
    ## Description

    [choose-date] December only

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "choose-date-easy"


class ChooseDateMediumEnv(MiniWoBEnvironment):
    """
    ## Description

    [choose-date] December or November only

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "choose-date-medium"


class ChooseDateNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [choose-date]

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "choose-date-nodelay"


class ChooseListEnv(MiniWoBEnvironment):
    """
    ## Description

    Choose an item from a drop down list.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "choose-list"


class CircleCenterEnv(MiniWoBEnvironment):
    """
    ## Description

    Find the center of a circle.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "circle-center"


class ClickButtonEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a specific button in a generated form.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-button"


class ClickButtonSequenceEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on buttons in a certain order.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-button-sequence"


class ClickCheckboxesEnv(MiniWoBEnvironment):
    """
    ## Description

    Click desired checkboxes.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-checkboxes"


class ClickCheckboxesLargeEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-checkboxes] Click at least 5 out of up to 12 checkboxes

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-checkboxes-large"


class ClickCheckboxesSoftEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-checkboxes] Paraphrased entries

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-checkboxes-soft"


class ClickCheckboxesTransferEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-checkboxes] Train and test on different number of targets

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-checkboxes-transfer"


class ClickCollapsibleEnv(MiniWoBEnvironment):
    """
    ## Description

    Click a collapsible element to expand it.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-collapsible"


class ClickCollapsible2Env(MiniWoBEnvironment):
    """
    ## Description

    Find and click on a specified link, from collapsible elements.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-collapsible-2"


class ClickCollapsible2NodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-collapsible-2]

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-collapsible-2-nodelay"


class ClickCollapsibleNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-collapsible]

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-collapsible-nodelay"


class ClickColorEnv(MiniWoBEnvironment):
    """
    ## Description

    Click the specified color.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-color"


class ClickDialogEnv(MiniWoBEnvironment):
    """
    ## Description

    Click the button to close the dialog box.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-dialog"


class ClickDialog2Env(MiniWoBEnvironment):
    """
    ## Description

    Click a specific button in a dialog box.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-dialog-2"


class ClickLinkEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a specified link in text.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-link"


class ClickMenuEnv(MiniWoBEnvironment):
    """
    ## Description

    Click menu items.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-menu"


class ClickMenu2Env(MiniWoBEnvironment):
    """
    ## Description

    Find a specific item from a menu.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-menu-2"


class ClickOptionEnv(MiniWoBEnvironment):
    """
    ## Description

    Click option boxes.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-option"


class ClickPieEnv(MiniWoBEnvironment):
    """
    ## Description

    Click items on a pie menu.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-pie"


class ClickPieNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-pie]

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-pie-nodelay"


class ClickScrollListEnv(MiniWoBEnvironment):
    """
    ## Description

    Click multiple items from a scroll list. (also require Shift + click)

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-scroll-list"


class ClickShadesEnv(MiniWoBEnvironment):
    """
    ## Description

    Click the shades that match a specified color.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-shades"


class ClickShapeEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a specific shape.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-shape"


class ClickTabEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a tab element.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-tab"


class ClickTab2Env(MiniWoBEnvironment):
    """
    ## Description

    Click a link inside a specific tab element.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-tab-2"


class ClickTab2EasyEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-tab-2] One 1 tab

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-tab-2-easy"


class ClickTab2HardEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-tab-2] Varying number of tabs from 2 to 6

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-tab-2-hard"


class ClickTab2MediumEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-tab-2] Choose between a link or "no match"

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-tab-2-medium"


class ClickTestEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a single button.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-test"


class ClickTest2Env(MiniWoBEnvironment):
    """
    ## Description

    Click on one of two buttons.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-test-2"


class ClickTestTransferEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-test] Different buttons during train and test

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-test-transfer"


class ClickWidgetEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a specific widget in a generated form.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "click-widget"


class CopyPasteEnv(MiniWoBEnvironment):
    """
    ## Description

    Copy text and paste it into an input.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "copy-paste"


class CopyPaste2Env(MiniWoBEnvironment):
    """
    ## Description

    Copy text from a specific textarea and paste it into an input.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "copy-paste-2"


class CountShapeEnv(MiniWoBEnvironment):
    """
    ## Description

    Count number of shapes.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "count-shape"


class CountSidesEnv(MiniWoBEnvironment):
    """
    ## Description

    Count the number of sides on a shape.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "count-sides"


class DragBoxEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag the smaller box into the larger box.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "drag-box"


class DragCubeEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag a 3D cube to show a specific face.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "drag-cube"


class DragItemsEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag items in a list, in a specified direction

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "drag-items"


class DragItemsGridEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag items in a 2D grid around.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "drag-items-grid"


class DragShapesEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag shapes into a box.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "drag-shapes"


class DragSortNumbersEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag numbers into sorted ascending order.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "drag-sort-numbers"


class EmailInboxEnv(MiniWoBEnvironment):
    """
    ## Description

    Navigate through an email inbox and perform some actions.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox"


class EmailInboxDeleteEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 1 subtask

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-delete"


class EmailInboxForwardEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 1 subtask

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-forward"


class EmailInboxForwardNlEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox-forward] NL instruction (30 templates)

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-forward-nl"


class EmailInboxForwardNlTurkEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox-forward] NL instruction (100 templates)

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-forward-nl-turk"


class EmailInboxImportantEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 1 subtask

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-important"


class EmailInboxNlTurkEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] NL instruction (100 templates for each subtask)

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-nl-turk"


class EmailInboxNoscrollEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-noscroll"


class EmailInboxReplyEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 1 subtask

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-reply"


class EmailInboxStarReplyEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 2 subtasks

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "email-inbox-star-reply"


class EnterDateEnv(MiniWoBEnvironment):
    """
    ## Description

    Use the date input to pick the correct date.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "enter-date"


class EnterPasswordEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter the password into the form.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "enter-password"


class EnterTextEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter given text to a textfield.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "enter-text"


class EnterText2Env(MiniWoBEnvironment):
    """
    ## Description

    Convert given text to upper or lower case.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "enter-text-2"


class EnterTextDynamicEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter dynamically generated text to a textfield.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "enter-text-dynamic"


class EnterTimeEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter the specified time into the input.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "enter-time"


class FindMidpointEnv(MiniWoBEnvironment):
    """
    ## Description

    Find the shortest mid-point of two points.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "find-midpoint"


class FindWordEnv(MiniWoBEnvironment):
    """
    ## Description

    Find nth word in a block of text.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "find-word"


class FocusTextEnv(MiniWoBEnvironment):
    """
    ## Description

    Focus into a text input.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "focus-text"


class FocusText2Env(MiniWoBEnvironment):
    """
    ## Description

    Focus on a specific text input.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "focus-text-2"


class GridCoordinateEnv(MiniWoBEnvironment):
    """
    ## Description

    Find the Cartesian coordinates on a grid.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "grid-coordinate"


class GuessNumberEnv(MiniWoBEnvironment):
    """
    ## Description

    Guess the number.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "guess-number"


class HighlightTextEnv(MiniWoBEnvironment):
    """
    ## Description

    Highlight all the text.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "highlight-text"


class HighlightText2Env(MiniWoBEnvironment):
    """
    ## Description

    Highlight the specified paragraph.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "highlight-text-2"


class IdentifyShapeEnv(MiniWoBEnvironment):
    """
    ## Description

    Identify a randomly generated shape.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "identify-shape"


class LoginUserEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter user login details into the form.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "login-user"


class LoginUserPopupEnv(MiniWoBEnvironment):
    """
    ## Description

    [login-user] Random popup

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "login-user-popup"


class MultiLayoutsEnv(MiniWoBEnvironment):
    """
    ## Description

    Fill in forms of varying layouts.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "multi-layouts"


class MultiOrderingsEnv(MiniWoBEnvironment):
    """
    ## Description

    Fill in forms with shuffled field orderings.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "multi-orderings"


class NavigateTreeEnv(MiniWoBEnvironment):
    """
    ## Description

    Navigate a file tree to find a specified file or folder.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "navigate-tree"


class NumberCheckboxesEnv(MiniWoBEnvironment):
    """
    ## Description

    Draw a given number using checkboxes.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "number-checkboxes"


class ReadTableEnv(MiniWoBEnvironment):
    """
    ## Description

    Read information out from a table.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "read-table"


class ReadTable2Env(MiniWoBEnvironment):
    """
    ## Description

    Read multiple pieces of information out from a table.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "read-table-2"


class ResizeTextareaEnv(MiniWoBEnvironment):
    """
    ## Description

    Resize a textarea in a given direction.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "resize-textarea"


class RightAngleEnv(MiniWoBEnvironment):
    """
    ## Description

    Given two points, add a third point to create a right angle.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "right-angle"


class ScrollTextEnv(MiniWoBEnvironment):
    """
    ## Description

    Scroll through a text area element and enter last word into text area.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "scroll-text"


class ScrollText2Env(MiniWoBEnvironment):
    """
    ## Description

    Scroll through a text area in a given direction.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "scroll-text-2"


class SearchEngineEnv(MiniWoBEnvironment):
    """
    ## Description

    Search through a bunch of results to find a specified link.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "search-engine"


class SimonSaysEnv(MiniWoBEnvironment):
    """
    ## Description

    Push the buttons in the order shown.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "simon-says"


class SimpleAlgebraEnv(MiniWoBEnvironment):
    """
    ## Description

    Solve for X.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "simple-algebra"


class SimpleArithmeticEnv(MiniWoBEnvironment):
    """
    ## Description

    Perform some arithmetic math operations.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "simple-arithmetic"


class SocialMediaEnv(MiniWoBEnvironment):
    """
    ## Description

    Interact with a social media feed.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "social-media"


class SocialMediaAllEnv(MiniWoBEnvironment):
    """
    ## Description

    [social-media] Do some action on all matching entries

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "social-media-all"


class SocialMediaSomeEnv(MiniWoBEnvironment):
    """
    ## Description

    [social-media] Do some action on some matching entries

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "social-media-some"


class TerminalEnv(MiniWoBEnvironment):
    """
    ## Description

    Use the terminal to delete a file.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "terminal"


class TextEditorEnv(MiniWoBEnvironment):
    """
    ## Description

    Modify a text"s style in a text-editor.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "text-editor"


class TextTransformEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter slightly transformed text into a text box.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "text-transform"


class TicTacToeEnv(MiniWoBEnvironment):
    """
    ## Description

    Win a game of tic-tac-toe.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "tic-tac-toe"


class UseAutocompleteEnv(MiniWoBEnvironment):
    """
    ## Description

    Use autocomplete element efficiently.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "use-autocomplete"


class UseAutocompleteNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [use-autocomplete]

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "use-autocomplete-nodelay"


class UseColorwheelEnv(MiniWoBEnvironment):
    """
    ## Description

    Use a color wheel.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "use-colorwheel"


class UseColorwheel2Env(MiniWoBEnvironment):
    """
    ## Description

    Use a color wheel given specific random color.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "use-colorwheel-2"


class UseSliderEnv(MiniWoBEnvironment):
    """
    ## Description

    Use a slider to select a particular value.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "use-slider"


class UseSlider2Env(MiniWoBEnvironment):
    """
    ## Description

    Use sliders to create a given combination.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "use-slider-2"


class UseSpinnerEnv(MiniWoBEnvironment):
    """
    ## Description

    Use a spinner to select given number.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "use-spinner"


class VisualAdditionEnv(MiniWoBEnvironment):
    """
    ## Description

    Count the total number of blocks.

    ## Example utterances

    * TODO

    ## Utterance fields

    * TODO

    ## Custom settings

    None
    """

    subdomain = "visual-addition"
