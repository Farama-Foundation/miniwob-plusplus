"""Environments for MiniWoB++ tasks."""

from miniwob.environment import MiniWoBEnvironment


class BisectAngleEnv(MiniWoBEnvironment):
    """
    ## Description

    Find the line that bisects an angle evenly in two.

    ## Example utterances

    * Create a line that bisects the angle evenly in two, then press submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "bisect-angle"


class BookFlightEnv(MiniWoBEnvironment):
    """
    ## Description

    Search for flight results.

    ## Example utterances

    * Book the cheapest one-way flight from: Anvik, AK to: NYC on 12/23/2016.
    * Book the cheapest one-way flight from: HIB to: SWD on 10/25/2016.
    * Book the cheapest one-way flight from: HKB to: Decatur, IL on 10/29/2016.
    * Book the shortest one-way flight from: Cincinnati, OH to: LEX on 10/16/2016.
    * Book the shortest one-way flight from: RAP to: ICT on 11/16/2016.

    ## Utterance fields

    * criterion
    * date
    * from
    * to

    ## Custom settings

    None
    """

    subdomain = "book-flight"


class BookFlightNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [book-flight]

    ## Example utterances

    * Book the cheapest one-way flight from: Anvik, AK to: NYC on 12/23/2016.
    * Book the cheapest one-way flight from: HIB to: SWD on 10/25/2016.
    * Book the cheapest one-way flight from: HKB to: Decatur, IL on 10/29/2016.
    * Book the shortest one-way flight from: Cincinnati, OH to: LEX on 10/16/2016.
    * Book the shortest one-way flight from: RAP to: ICT on 11/16/2016.

    ## Utterance fields

    * criterion
    * date
    * from
    * to

    ## Custom settings

    None
    """

    subdomain = "book-flight-nodelay"


class ChooseDateEnv(MiniWoBEnvironment):
    """
    ## Description

    Learn to operate a date picker tool.

    ## Example utterances

    * Select 01/14/2016 as the date and hit submit.
    * Select 03/05/2016 as the date and hit submit.
    * Select 05/15/2016 as the date and hit submit.
    * Select 05/17/2016 as the date and hit submit.
    * Select 10/03/2016 as the date and hit submit.

    ## Utterance fields

    * day
    * month
    * year

    ## Custom settings

    None
    """

    subdomain = "choose-date"


class ChooseDateEasyEnv(MiniWoBEnvironment):
    """
    ## Description

    [choose-date] December only

    ## Example utterances

    * Select 12/02/2016 as the date and hit submit.
    * Select 12/06/2016 as the date and hit submit.
    * Select 12/12/2016 as the date and hit submit.
    * Select 12/23/2016 as the date and hit submit.
    * Select 12/27/2016 as the date and hit submit.

    ## Utterance fields

    * day
    * month
    * year

    ## Custom settings

    None
    """

    subdomain = "choose-date-easy"


class ChooseDateMediumEnv(MiniWoBEnvironment):
    """
    ## Description

    [choose-date] December or November only

    ## Example utterances

    * Select 11/03/2016 as the date and hit submit.
    * Select 11/11/2016 as the date and hit submit.
    * Select 11/23/2016 as the date and hit submit.
    * Select 12/16/2016 as the date and hit submit.
    * Select 12/24/2016 as the date and hit submit.

    ## Utterance fields

    * day
    * month
    * year

    ## Custom settings

    None
    """

    subdomain = "choose-date-medium"


class ChooseDateNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [choose-date]

    ## Example utterances

    * Select 01/14/2016 as the date and hit submit.
    * Select 03/05/2016 as the date and hit submit.
    * Select 05/15/2016 as the date and hit submit.
    * Select 05/17/2016 as the date and hit submit.
    * Select 10/03/2016 as the date and hit submit.

    ## Utterance fields

    * day
    * month
    * year

    ## Custom settings

    None
    """

    subdomain = "choose-date-nodelay"


class ChooseListEnv(MiniWoBEnvironment):
    """
    ## Description

    Choose an item from a drop down list.

    ## Example utterances

    * Select Betty from the list and click Submit.
    * Select Bobine from the list and click Submit.
    * Select Ferne from the list and click Submit.
    * Select Heard Island and McDonald Islands from the list and click Submit.
    * Select Helli from the list and click Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "choose-list"


class CircleCenterEnv(MiniWoBEnvironment):
    """
    ## Description

    Find the center of a circle.

    ## Example utterances

    * Find and click on the center of the circle, then press submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "circle-center"


class ClickButtonEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a specific button in a generated form.

    ## Example utterances

    * Click on the "Ok" button.
    * Click on the "no" button.
    * Click on the "ok" button.
    * Click on the "okay" button.
    * Click on the "submit" button.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-button"


class ClickButtonSequenceEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on buttons in a certain order.

    ## Example utterances

    * Click button ONE, then click button TWO.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "click-button-sequence"


class ClickCheckboxesEnv(MiniWoBEnvironment):
    """
    ## Description

    Click desired checkboxes.

    ## Example utterances

    * Select 91YPF, i6Vdpn2, nd7Qt, XPMut and click Submit.
    * Select DKkQH and click Submit.
    * Select HF2 and click Submit.
    * Select fzzqo, NYYyS82 and click Submit.
    * Select nothing and click Submit.

    ## Utterance fields

    * button
    * target 0
    * target 1
    * target 2
    * target 3

    ## Custom settings

    None
    """

    subdomain = "click-checkboxes"


class ClickCheckboxesLargeEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-checkboxes] Click at least 5 out of up to 12 checkboxes

    ## Example utterances

    * Select 4aycHnY, 1YPFe2i, gbQ4S2, Vdpn2dP, OX, Mutiv, d7Qt, fwDwN, ZH2tL1, UJWGA, pRdsyR and click Submit.
    * Select 7jRPftZ, 5WZHv, TvFgM, yZZUALj, nXH, EoPV, qtdjmII, Q0af and click Submit.
    * Select k9, Kh, zzq, key, bA2, gZf3, nhG97 and click Submit.
    * Select kQHh8j, SaIGD, wjy8, 4tF, oB, 2uMiJWr and click Submit.
    * Select nb, 8qiSp3m, pKybC69, v8Zs3, U6gHF and click Submit.

    ## Utterance fields

    * button
    * target 0
    * target 1
    * target 10
    * target 11
    * target 2
    * target 3
    * target 4
    * target 5
    * target 6
    * target 7
    * target 8
    * target 9

    ## Custom settings

    None
    """

    subdomain = "click-checkboxes-large"


class ClickCheckboxesSoftEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-checkboxes] Paraphrased entries

    ## Example utterances

    * Select words similar to brave, chubby, depraved and click Submit.
    * Select words similar to gleeful, swine, rabbits, flames and click Submit.
    * Select words similar to mild, delicious and click Submit.
    * Select words similar to red and click Submit.
    * Select words similar to response, panicked and click Submit.

    ## Utterance fields

    * button
    * target 0
    * target 1
    * target 2
    * target 3
    * target 4

    ## Custom settings

    None
    """

    subdomain = "click-checkboxes-soft"


class ClickCheckboxesTransferEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-checkboxes] Train and test on different number of targets

    ## Example utterances

    * Select FBYPK4g, coN4Zj, ICsb and click Submit.
    * Select Mutiv, d7Qt, OX and click Submit.
    * Select ZV6g and click Submit.
    * Select k9 and click Submit.
    * Select nothing and click Submit.

    ## Utterance fields

    * button
    * target 0
    * target 1
    * target 2

    ## Custom settings

    None
    """

    subdomain = "click-checkboxes-transfer"


class ClickCollapsibleEnv(MiniWoBEnvironment):
    """
    ## Description

    Click a collapsible element to expand it.

    ## Example utterances

    * Expand the section below and click submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "click-collapsible"


class ClickCollapsible2Env(MiniWoBEnvironment):
    """
    ## Description

    Find and click on a specified link, from collapsible elements.

    ## Example utterances

    * Expand the sections below, to find and click on the link "Habitasse".
    * Expand the sections below, to find and click on the link "ac".
    * Expand the sections below, to find and click on the link "aliquet".
    * Expand the sections below, to find and click on the link "euismod.".
    * Expand the sections below, to find and click on the link "mattis".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-collapsible-2"


class ClickCollapsible2NodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-collapsible-2]

    ## Example utterances

    * Expand the sections below, to find and click on the link "Habitasse".
    * Expand the sections below, to find and click on the link "ac".
    * Expand the sections below, to find and click on the link "aliquet".
    * Expand the sections below, to find and click on the link "euismod.".
    * Expand the sections below, to find and click on the link "mattis".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-collapsible-2-nodelay"


class ClickCollapsibleNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-collapsible]

    ## Example utterances

    * Expand the section below and click submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "click-collapsible-nodelay"


class ClickColorEnv(MiniWoBEnvironment):
    """
    ## Description

    Click the specified color.

    ## Example utterances

    * Click on the cyan colored box.
    * Click on the grey colored box.
    * Click on the olive colored box.
    * Click on the white colored box.
    * Click on the yellow colored box.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-color"


class ClickDialogEnv(MiniWoBEnvironment):
    """
    ## Description

    Click the button to close the dialog box.

    ## Example utterances

    * Close the dialog box by clicking the "x".

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "click-dialog"


class ClickDialog2Env(MiniWoBEnvironment):
    """
    ## Description

    Click a specific button in a dialog box.

    ## Example utterances

    * Click the button in the dialog box labeled "Cancel".
    * Click the button in the dialog box labeled "OK".
    * Click the button in the dialog box labeled "x".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-dialog-2"


class ClickLinkEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a specified link in text.

    ## Example utterances

    * Click on the link "Eget".
    * Click on the link "blandit".
    * Click on the link "nam".
    * Click on the link "porttitor".
    * Click on the link "sed".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-link"


class ClickMenuEnv(MiniWoBEnvironment):
    """
    ## Description

    Click menu items.

    ## Example utterances

    * Select Almira>Sherye>Anissa
    * Select Alvera>Terza>Ludovika
    * Select Diandra>Mollie>Velma
    * Select Evy>Tammara
    * Select Martelle

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-menu"


class ClickMenu2Env(MiniWoBEnvironment):
    """
    ## Description

    Find a specific item from a menu.

    ## Example utterances

    * Click the "Menu" button, and then find and click on the item labeled "Next".
    * Click the "Menu" button, and then find and click on the item labeled "Prev".
    * Click the "Menu" button, and then find and click on the item labeled "Save".
    * Click the "Menu" button, and then find and click on the item labeled "Zoom Out".
    * Click the "Menu" button, and then find and click on the item with the icon.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-menu-2"


class ClickOptionEnv(MiniWoBEnvironment):
    """
    ## Description

    Click option boxes.

    ## Example utterances

    * Select AU and click Submit.
    * Select GDKkQ and click Submit.
    * Select Vdpn2dP and click Submit.
    * Select nZV6g2 and click Submit.
    * Select yS82i and click Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-option"


class ClickPieEnv(MiniWoBEnvironment):
    """
    ## Description

    Click items on a pie menu.

    ## Example utterances

    * Expand the pie menu below and click on the item labeled "7".
    * Expand the pie menu below and click on the item labeled "A".
    * Expand the pie menu below and click on the item labeled "S".
    * Expand the pie menu below and click on the item labeled "e".
    * Expand the pie menu below and click on the item labeled "f".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-pie"


class ClickPieNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-pie]

    ## Example utterances

    * Expand the pie menu below and click on the item labeled "7".
    * Expand the pie menu below and click on the item labeled "A".
    * Expand the pie menu below and click on the item labeled "S".
    * Expand the pie menu below and click on the item labeled "e".
    * Expand the pie menu below and click on the item labeled "f".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-pie-nodelay"


class ClickScrollListEnv(MiniWoBEnvironment):
    """
    ## Description

    Click multiple items from a scroll list. (also require Shift + click)

    ## Example utterances

    * Select Christal from the scroll list and click Submit.
    * Select Coleen from the scroll list and click Submit.
    * Select Corrine, Catherine from the scroll list and click Submit.
    * Select Heard Island and McDonald Islands, Nicaragua from the scroll list and click Submit.
    * Select Ronda from the scroll list and click Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-scroll-list"


class ClickShadesEnv(MiniWoBEnvironment):
    """
    ## Description

    Click the shades that match a specified color.

    ## Example utterances

    * Select all the shades of blue and press Submit.
    * Select all the shades of green and press Submit.
    * Select all the shades of red and press Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-shades"


class ClickShapeEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a specific shape.

    ## Example utterances

    * Click on a 9
    * Click on a aqua item
    * Click on a large digit
    * Click on a small green shape
    * Click on a small letter

    ## Utterance fields

    * color
    * size
    * target
    * type

    ## Custom settings

    None
    """

    subdomain = "click-shape"


class ClickTabEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a tab element.

    ## Example utterances

    * Click on Tab #1.
    * Click on Tab #2.
    * Click on Tab #3.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-tab"


class ClickTab2Env(MiniWoBEnvironment):
    """
    ## Description

    Click a link inside a specific tab element.

    ## Example utterances

    * Switch between the tabs to find and click on the link "Habitasse".
    * Switch between the tabs to find and click on the link "ac".
    * Switch between the tabs to find and click on the link "aliquet".
    * Switch between the tabs to find and click on the link "euismod.".
    * Switch between the tabs to find and click on the link "mattis".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-tab-2"


class ClickTab2EasyEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-tab-2] One 1 tab

    ## Example utterances

    * Switch between the tabs to find and click on the link "Eget".
    * Switch between the tabs to find and click on the link "blandit".
    * Switch between the tabs to find and click on the link "nam".
    * Switch between the tabs to find and click on the link "porttitor".
    * Switch between the tabs to find and click on the link "sed".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-tab-2-easy"


class ClickTab2HardEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-tab-2] Varying number of tabs from 2 to 6

    ## Example utterances

    * Switch between the tabs to find and click on the link "Duis".
    * Switch between the tabs to find and click on the link "Sed".
    * Switch between the tabs to find and click on the link "Viverra".
    * Switch between the tabs to find and click on the link "lectus".
    * Switch between the tabs to find and click on the link "vulputate.".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-tab-2-hard"


class ClickTab2MediumEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-tab-2] Choose between a link or "no match"

    ## Example utterances

    * Switch between the tabs to find and click on the link "Congue.".
    * Switch between the tabs to find and click on the link "Nisl".
    * Switch between the tabs to find and click on the link "aliquet".
    * Switch between the tabs to find and click on the link "justo.".
    * Switch between the tabs to find and click on the link "mattis".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-tab-2-medium"


class ClickTestEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a single button.

    ## Example utterances

    * Click the button.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "click-test"


class ClickTest2Env(MiniWoBEnvironment):
    """
    ## Description

    Click on one of two buttons.

    ## Example utterances

    * Click button ONE.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-test-2"


class ClickTestTransferEnv(MiniWoBEnvironment):
    """
    ## Description

    [click-test] Different buttons during train and test

    ## Example utterances

    * Click button ONE.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-test-transfer"


class ClickWidgetEnv(MiniWoBEnvironment):
    """
    ## Description

    Click on a specific widget in a generated form.

    ## Example utterances

    * Click on a "button" widget.
    * Click on a "checkbox" widget.
    * Click on a "radio" widget.
    * Click on a "text" widget.
    * Click on a "textarea" widget.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "click-widget"


class CopyPasteEnv(MiniWoBEnvironment):
    """
    ## Description

    Copy text and paste it into an input.

    ## Example utterances

    * Copy the text in the textarea below, paste it into the textbox and press Submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "copy-paste"


class CopyPaste2Env(MiniWoBEnvironment):
    """
    ## Description

    Copy text from a specific textarea and paste it into an input.

    ## Example utterances

    * Copy the text from the 1st text area below and paste it into the text input, then press Submit.
    * Copy the text from the 2nd text area below and paste it into the text input, then press Submit.
    * Copy the text from the 3rd text area below and paste it into the text input, then press Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "copy-paste-2"


class CountShapeEnv(MiniWoBEnvironment):
    """
    ## Description

    Count number of shapes.

    ## Example utterances

    * How many aqua items are there?
    * How many large yellow items are there?
    * How many red digits are there?
    * How many shapes are there?
    * How many small green items are there?

    ## Utterance fields

    * color
    * size
    * target
    * type

    ## Custom settings

    None
    """

    subdomain = "count-shape"


class CountSidesEnv(MiniWoBEnvironment):
    """
    ## Description

    Count the number of sides on a shape.

    ## Example utterances

    * Press the button that correctly denotes how many sides the shape has.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "count-sides"


class DragBoxEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag the smaller box into the larger box.

    ## Example utterances

    * Drag the smaller box so that it is completely inside the larger box.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "drag-box"


class DragCircleEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag an item in a specified direction.

    ## Example utterances

    * Drag the circle down then press Submit.
    * Drag the circle left then press Submit.
    * Drag the circle right then press Submit.
    * Drag the circle up then press Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "drag-circle"


class DragCubeEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag a 3D cube to show a specific face.

    ## Example utterances

    * Move the cube around so that "1" is the active side facing the user.
    * Move the cube around so that "2" is the active side facing the user.
    * Move the cube around so that "3" is the active side facing the user.
    * Move the cube around so that "5" is the active side facing the user.
    * Move the cube around so that "6" is the active side facing the user.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "drag-cube"


class DragItemsEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag items in a list, in a specified direction

    ## Example utterances

    * Drag Gerda to the 3rd position.
    * Drag Jerrilyn to the 1st position.
    * Drag Margette down by one position.
    * Drag Sara-Ann to the 1st position.
    * Drag Theodosia to the 3rd position.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "drag-items"


class DragItemsGridEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag items in a 2D grid around.

    ## Example utterances

    * Drag Andria to the top right.
    * Drag Drucy up by one.
    * Drag Marcille to the bottom right.
    * Drag Marta to the bottom center.
    * Drag Vally to the bottom center.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "drag-items-grid"


class DragShapesEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag shapes into a box.

    ## Example utterances

    * Drag all circles into the black box.
    * Drag all rectangles into the black box.
    * Drag all triangles into the black box.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "drag-shapes"


class DragSortNumbersEnv(MiniWoBEnvironment):
    """
    ## Description

    Drag numbers into sorted ascending order.

    ## Example utterances

    * Sort the numbers in increasing order, starting with the lowest number at the top of the list.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "drag-sort-numbers"


class EmailInboxEnv(MiniWoBEnvironment):
    """
    ## Description

    Navigate through an email inbox and perform some actions.

    ## Example utterances

    * Find the email by Audrey and forward that email to Hedy.
    * Find the email by Bettine and reply to them with the text "Gravida.".
    * Find the email by Cathrine and click the star icon to mark it as important.
    * Find the email by Jemima and reply to them with the text "Purus velit faucibus eu.".
    * Find the email by Valida and reply to them with the text "Risus augue odio turpis.".

    ## Utterance fields

    * by
    * message
    * task
    * to

    ## Custom settings

    None
    """

    subdomain = "email-inbox"


class EmailInboxDeleteEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 1 subtask

    ## Example utterances

    * Find the email by Audrey and click the trash icon to delete it.
    * Find the email by Coletta and click the trash icon to delete it.
    * Find the email by Danice and click the trash icon to delete it.
    * Find the email by Gerta and click the trash icon to delete it.
    * Find the email by Goldina and click the trash icon to delete it.

    ## Utterance fields

    * by
    * task

    ## Custom settings

    None
    """

    subdomain = "email-inbox-delete"


class EmailInboxForwardEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 1 subtask

    ## Example utterances

    * Find the email by Audrey and forward that email to Orel.
    * Find the email by Coletta and forward that email to Odette.
    * Find the email by Danice and forward that email to Camel.
    * Find the email by Gerta and forward that email to Marna.
    * Find the email by Goldina and forward that email to Judith.

    ## Utterance fields

    * by
    * task
    * to

    ## Custom settings

    None
    """

    subdomain = "email-inbox-forward"


class EmailInboxForwardNlEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox-forward] NL instruction (30 templates)

    ## Example utterances

    * Amargo is waiting for the email by Lissie.
    * Forward to Cathrine the email from Evy.
    * Give Bobine the message you received from Cora,
    * Please forward to Delores the email by Valida.
    * Send Bettine the information Lidia sent to you.

    ## Utterance fields

    * by
    * to

    ## Custom settings

    None
    """

    subdomain = "email-inbox-forward-nl"


class EmailInboxForwardNlTurkEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox-forward] NL instruction (100 templates)

    ## Example utterances

    * Amargo wrote an email in this app that needs to be forwarded to Penelope.
    * Find Coletta's email and send it to Evy.
    * Look for the email that Bobine wrote in this email app and forward it to Bevvy
    * Open Patsy's email and forward it to Delores
    * Will you find the email from Kiley and forward it to Sibylla?

    ## Utterance fields

    * by
    * to

    ## Custom settings

    None
    """

    subdomain = "email-inbox-forward-nl-turk"


class EmailInboxImportantEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 1 subtask

    ## Example utterances

    * Find the email by Audrey and click the star icon to mark it as important.
    * Find the email by Coletta and click the star icon to mark it as important.
    * Find the email by Danice and click the star icon to mark it as important.
    * Find the email by Gerta and click the star icon to mark it as important.
    * Find the email by Goldina and click the star icon to mark it as important.

    ## Utterance fields

    * by
    * task

    ## Custom settings

    None
    """

    subdomain = "email-inbox-important"


class EmailInboxNlTurkEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] NL instruction (100 templates for each subtask)

    ## Example utterances

    * Bobine's email should be deleted from the inbox.
    * Delete all messages from Coletta.
    * Email Kiley the message, "Amet, a. Malesuada. Nunc."
    * Please delete Amargo's emails.
    * Please find the email Patsy sent me and file it as important

    ## Utterance fields

    * by
    * message
    * task
    * to

    ## Custom settings

    None
    """

    subdomain = "email-inbox-nl-turk"


class EmailInboxNoscrollEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling

    ## Example utterances

    * Find the email by Audrey and forward that email to Orel.
    * Find the email by Coletta and reply to them with the text "Odio fermentum quam auctor.".
    * Find the email by Danice and click the trash icon to delete it.
    * Find the email by Gerta and click the trash icon to delete it.
    * Find the email by Goldina and click the star icon to mark it as important.

    ## Utterance fields

    * by
    * message
    * task
    * to

    ## Custom settings

    None
    """

    subdomain = "email-inbox-noscroll"


class EmailInboxReplyEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 1 subtask

    ## Example utterances

    * Find the email by Audrey and reply to them with the text "Vel quis. Semper.".
    * Find the email by Coletta and reply to them with the text "Odio fermentum quam auctor.".
    * Find the email by Danice and reply to them with the text "Aenean.".
    * Find the email by Gerta and reply to them with the text "Ac sit non.".
    * Find the email by Goldina and reply to them with the text "At non lacus.".

    ## Utterance fields

    * by
    * message
    * task

    ## Custom settings

    None
    """

    subdomain = "email-inbox-reply"


class EmailInboxStarReplyEnv(MiniWoBEnvironment):
    """
    ## Description

    [email-inbox] No scrolling + 2 subtasks

    ## Example utterances

    * Find the email by Audrey and reply to them with the text "Vel quis. Semper.".
    * Find the email by Coletta and reply to them with the text "Odio fermentum quam auctor.".
    * Find the email by Danice and click the star icon to mark it as important.
    * Find the email by Gerta and click the star icon to mark it as important.
    * Find the email by Goldina and click the star icon to mark it as important.

    ## Utterance fields

    * by
    * message
    * task

    ## Custom settings

    None
    """

    subdomain = "email-inbox-star-reply"


class EnterDateEnv(MiniWoBEnvironment):
    """
    ## Description

    Use the date input to pick the correct date.

    ## Example utterances

    * Enter 05/20/2010 as the date and hit submit.
    * Enter 07/26/2017 as the date and hit submit.
    * Enter 09/17/2013 as the date and hit submit.
    * Enter 10/02/2013 as the date and hit submit.
    * Enter 10/11/2011 as the date and hit submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "enter-date"


class EnterPasswordEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter the password into the form.

    ## Example utterances

    * Enter the password "817" into both text fields and press submit.
    * Enter the password "D91YP" into both text fields and press submit.
    * Enter the password "Sfz" into both text fields and press submit.
    * Enter the password "fU" into both text fields and press submit.
    * Enter the password "yA" into both text fields and press submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "enter-password"


class EnterTextEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter given text to a textfield.

    ## Example utterances

    * Enter "Agustina" into the text field and press Submit.
    * Enter "Ignacio" into the text field and press Submit.
    * Enter "Jerald" into the text field and press Submit.
    * Enter "Marcella" into the text field and press Submit.
    * Enter "Myron" into the text field and press Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "enter-text"


class EnterText2Env(MiniWoBEnvironment):
    """
    ## Description

    Convert given text to upper or lower case.

    ## Example utterances

    * Type "IGNACIO" in all lower case letters in the text input and press Submit.
    * Type "JERALD" in all lower case letters in the text input and press Submit.
    * Type "MARCELLA" in all lower case letters in the text input and press Submit.
    * Type "agustina" in all upper case letters in the text input and press Submit.
    * Type "myron" in all upper case letters in the text input and press Submit.

    ## Utterance fields

    * case
    * text

    ## Custom settings

    None
    """

    subdomain = "enter-text-2"


class EnterTextDynamicEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter dynamically generated text to a textfield.

    ## Example utterances

    * Enter "6gH" into the text field and press Submit.
    * Enter "YPFe2" into the text field and press Submit.
    * Enter "aIGD" into the text field and press Submit.
    * Enter "jRPft" into the text field and press Submit.
    * Enter "zq" into the text field and press Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "enter-text-dynamic"


class EnterTimeEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter the specified time into the input.

    ## Example utterances

    * Enter 12:25 AM as the time and press submit.
    * Enter 12:34 PM as the time and press submit.
    * Enter 7:01 AM as the time and press submit.
    * Enter 8:04 PM as the time and press submit.
    * Enter 9:37 PM as the time and press submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "enter-time"


class FindMidpointEnv(MiniWoBEnvironment):
    """
    ## Description

    Find the shortest mid-point of two points.

    ## Example utterances

    * Find and click on the shortest mid-point between the two points, then press submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "find-midpoint"


class FindWordEnv(MiniWoBEnvironment):
    """
    ## Description

    Find nth word in a block of text.

    ## Example utterances

    * Find the 1st word in the paragraph, type that into the textbox and press "Submit".
    * Find the 2nd word in the paragraph, type that into the textbox and press "Submit".
    * Find the 6th word in the paragraph, type that into the textbox and press "Submit".
    * Find the 8th word in the paragraph, type that into the textbox and press "Submit".
    * Find the 9th word in the paragraph, type that into the textbox and press "Submit".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "find-word"


class FocusTextEnv(MiniWoBEnvironment):
    """
    ## Description

    Focus into a text input.

    ## Example utterances

    * Focus into the textbox.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "focus-text"


class FocusText2Env(MiniWoBEnvironment):
    """
    ## Description

    Focus on a specific text input.

    ## Example utterances

    * Focus into the 1st input textbox.
    * Focus into the 2nd input textbox.
    * Focus into the 3rd input textbox.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "focus-text-2"


class GridCoordinateEnv(MiniWoBEnvironment):
    """
    ## Description

    Find the Cartesian coordinates on a grid.

    ## Example utterances

    * Click on the grid coordinate (-1,1).
    * Click on the grid coordinate (-1,2).
    * Click on the grid coordinate (-2,-1).
    * Click on the grid coordinate (-2,-2).
    * Click on the grid coordinate (1,1).

    ## Utterance fields

    * x
    * y

    ## Custom settings

    None
    """

    subdomain = "grid-coordinate"


class GuessNumberEnv(MiniWoBEnvironment):
    """
    ## Description

    Guess the number.

    ## Example utterances

    * Guess the number between 0-9 and press Submit. Use the feedback below to find the right number.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "guess-number"


class HighlightTextEnv(MiniWoBEnvironment):
    """
    ## Description

    Highlight all the text.

    ## Example utterances

    * Highlight the text in the paragraph below and click submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "highlight-text"


class HighlightText2Env(MiniWoBEnvironment):
    """
    ## Description

    Highlight the specified paragraph.

    ## Example utterances

    * Highlight the text in the 1st paragraph and click submit.
    * Highlight the text in the 2nd paragraph and click submit.
    * Highlight the text in the 3rd paragraph and click submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "highlight-text-2"


class IdentifyShapeEnv(MiniWoBEnvironment):
    """
    ## Description

    Identify a randomly generated shape.

    ## Example utterances

    * Click the button that best describes the figure below.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "identify-shape"


class LoginUserEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter user login details into the form.

    ## Example utterances

    * Enter the username "karrie" and the password "AU" into the text fields and press login.
    * Enter the username "keneth" and the password "91YP" into the text fields and press login.
    * Enter the username "nathalie" and the password "17jRP" into the text fields and press login.
    * Enter the username "nathalie" and the password "fzzq" into the text fields and press login.
    * Enter the username "vina" and the password "US" into the text fields and press login.

    ## Utterance fields

    * password
    * username

    ## Custom settings

    None
    """

    subdomain = "login-user"


class LoginUserPopupEnv(MiniWoBEnvironment):
    """
    ## Description

    [login-user] Random popup

    ## Example utterances

    * Enter the username "karrie" and the password "AU" into the text fields and press login.
    * Enter the username "keneth" and the password "91YP" into the text fields and press login.
    * Enter the username "nathalie" and the password "17jRP" into the text fields and press login.
    * Enter the username "nathalie" and the password "fzzq" into the text fields and press login.
    * Enter the username "vina" and the password "US" into the text fields and press login.

    ## Utterance fields

    * password
    * username

    ## Custom settings

    None
    """

    subdomain = "login-user-popup"


class MultiLayoutsEnv(MiniWoBEnvironment):
    """
    ## Description

    Fill in forms of varying layouts.

    ## Example utterances

    * Search for action movies directed by Bowen from year 1998.
    * Search for crime movies directed by Curry from year 1995.
    * Search for historical movies directed by Mcknight from year 1980.
    * Search for historical movies directed by West from year 2010.
    * Search for satire movies directed by Mejia from year 2017.

    ## Utterance fields

    * director
    * genre
    * year

    ## Custom settings

    None
    """

    subdomain = "multi-layouts"


class MultiOrderingsEnv(MiniWoBEnvironment):
    """
    ## Description

    Fill in forms with shuffled field orderings.

    ## Example utterances

    * Search for action movies directed by Bowen from year 1998.
    * Search for crime movies directed by Curry from year 1995.
    * Search for historical movies directed by Mcknight from year 1980.
    * Search for historical movies directed by West from year 2010.
    * Search for satire movies directed by Mejia from year 2017.

    ## Utterance fields

    * director
    * genre
    * year

    ## Custom settings

    None
    """

    subdomain = "multi-orderings"


class NavigateTreeEnv(MiniWoBEnvironment):
    """
    ## Description

    Navigate a file tree to find a specified file or folder.

    ## Example utterances

    * Navigate through the file tree. Find and click on the folder or file named "Agustina".
    * Navigate through the file tree. Find and click on the folder or file named "Annis".
    * Navigate through the file tree. Find and click on the folder or file named "Briana".
    * Navigate through the file tree. Find and click on the folder or file named "Deneen".
    * Navigate through the file tree. Find and click on the folder or file named "Truman".

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "navigate-tree"


class NumberCheckboxesEnv(MiniWoBEnvironment):
    """
    ## Description

    Draw a given number using checkboxes.

    ## Example utterances

    * Draw the number "0" in the checkboxes using the example on the right and press Submit when finished.
    * Draw the number "1" in the checkboxes using the example on the right and press Submit when finished.
    * Draw the number "3" in the checkboxes using the example on the right and press Submit when finished.
    * Draw the number "7" in the checkboxes using the example on the right and press Submit when finished.
    * Draw the number "8" in the checkboxes using the example on the right and press Submit when finished.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "number-checkboxes"


class ReadTableEnv(MiniWoBEnvironment):
    """
    ## Description

    Read information out from a table.

    ## Example utterances

    * Enter the value of Color into the text field and press Submit.
    * Enter the value of Country into the text field and press Submit.
    * Enter the value of Language into the text field and press Submit.
    * Enter the value of Last name into the text field and press Submit.
    * Enter the value of Religion into the text field and press Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "read-table"


class ReadTable2Env(MiniWoBEnvironment):
    """
    ## Description

    Read multiple pieces of information out from a table.

    ## Example utterances

    * Enter the value that corresponds with each label into the form and submit when done.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "read-table-2"


class ResizeTextareaEnv(MiniWoBEnvironment):
    """
    ## Description

    Resize a textarea in a given direction.

    ## Example utterances

    * Resize the textarea so that the height is larger than its initial size then press Submit.
    * Resize the textarea so that the height is smaller than its initial size then press Submit.
    * Resize the textarea so that the width is larger than its initial size then press Submit.
    * Resize the textarea so that the width is smaller than its initial size then press Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "resize-textarea"


class RightAngleEnv(MiniWoBEnvironment):
    """
    ## Description

    Given two points, add a third point to create a right angle.

    ## Example utterances

    * Add a third point to create a right angle, then press submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "right-angle"


class ScrollTextEnv(MiniWoBEnvironment):
    """
    ## Description

    Scroll through a text area element and enter last word into text area.

    ## Example utterances

    * Find the last word in the text area, enter it into the text field and hit Submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "scroll-text"


class ScrollText2Env(MiniWoBEnvironment):
    """
    ## Description

    Scroll through a text area in a given direction.

    ## Example utterances

    * Scroll the textarea to the bottom of the text hit submit.
    * Scroll the textarea to the top of the text hit submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "scroll-text-2"


class SearchEngineEnv(MiniWoBEnvironment):
    """
    ## Description

    Search through a bunch of results to find a specified link.

    ## Example utterances

    * Use the textbox to enter "Dolores" and press "Search", then find and click the 7th search result.
    * Use the textbox to enter "Kanesha" and press "Search", then find and click the 4th search result.
    * Use the textbox to enter "Nathalie" and press "Search", then find and click the 1st search result.
    * Use the textbox to enter "Renda" and press "Search", then find and click the 7th search result.
    * Use the textbox to enter "Riley" and press "Search", then find and click the 7th search result.

    ## Utterance fields

    * query
    * rank

    ## Custom settings

    None
    """

    subdomain = "search-engine"


class SimpleAlgebraEnv(MiniWoBEnvironment):
    """
    ## Description

    Solve for X.

    ## Example utterances

    * Solve for x and type your answer into the textbox. Press Submit when done.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "simple-algebra"


class SimpleArithmeticEnv(MiniWoBEnvironment):
    """
    ## Description

    Perform some arithmetic math operations.

    ## Example utterances

    * Solve the math problem and type your answer into the textbox. Press submit when done.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "simple-arithmetic"


class SocialMediaEnv(MiniWoBEnvironment):
    """
    ## Description

    Interact with a social media feed.

    ## Example utterances

    * For the user @consectetur, click on the "Block" button.
    * For the user @emile, click on the "Embed Tweet" button.
    * For the user @leo, click on the "Mute" button.
    * For the user @leo, click on the "Share via DM" button.
    * For the user @nec, click on the "Share via DM" button.

    ## Utterance fields

    * button
    * user

    ## Custom settings

    None
    """

    subdomain = "social-media"


class SocialMediaAllEnv(MiniWoBEnvironment):
    """
    ## Description

    [social-media] Do some action on all matching entries

    ## Example utterances

    * Click the "Like" button on all posts by @deneen and then click Submit.
    * Click the "Reply" button on all posts by @dis and then click Submit.
    * Click the "Retweet" button on all posts by @leonie and then click Submit.
    * Click the "Share" button on all posts by @annis and then click Submit.
    * Click the "Share" button on all posts by @egestas and then click Submit.

    ## Utterance fields

    * button
    * submit
    * user

    ## Custom settings

    None
    """

    subdomain = "social-media-all"


class SocialMediaSomeEnv(MiniWoBEnvironment):
    """
    ## Description

    [social-media] Do some action on some matching entries

    ## Example utterances

    * Click the "Like" button on 5 posts by @deneen and then click Submit.
    * Click the "Reply" button on 2 posts by @dis and then click Submit.
    * Click the "Retweet" button on 3 posts by @leonie and then click Submit.
    * Click the "Share" button on 1 post by @annis and then click Submit.
    * Click the "Share" button on 8 posts by @egestas and then click Submit.

    ## Utterance fields

    * amount
    * button
    * submit
    * user

    ## Custom settings

    None
    """

    subdomain = "social-media-some"


class TerminalEnv(MiniWoBEnvironment):
    """
    ## Description

    Use the terminal to delete a file.

    ## Example utterances

    * Use the terminal below to delete a file ending with the extension .gif
    * Use the terminal below to delete a file ending with the extension .gpg
    * Use the terminal below to delete a file ending with the extension .rb
    * Use the terminal below to delete a file ending with the extension .tar.gz
    * Use the terminal below to delete a file that has no file extension.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "terminal"


class TextEditorEnv(MiniWoBEnvironment):
    """
    ## Description

    Modify a text"s style in a text-editor.

    ## Example utterances

    * Using the text editor, give everything the style bold and press Submit.
    * Using the text editor, give everything the style italics and press Submit.
    * Using the text editor, give everything the style underlined and press Submit.
    * Using the text editor, give the text magna. the style bold and press Submit.
    * Using the text editor, give the text sed the color yellow.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "text-editor"


class TextTransformEnv(MiniWoBEnvironment):
    """
    ## Description

    Enter slightly transformed text into a text box.

    ## Example utterances

    * Type the text below into the text field and press Submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "text-transform"


class TicTacToeEnv(MiniWoBEnvironment):
    """
    ## Description

    Win a game of tic-tac-toe.

    ## Example utterances

    * Playing as 'X', win a game of tic-tac-toe.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "tic-tac-toe"


class UseAutocompleteEnv(MiniWoBEnvironment):
    """
    ## Description

    Use autocomplete element efficiently.

    ## Example utterances

    * Enter an item that starts with "An" and ends with "ica".
    * Enter an item that starts with "Ce" and ends with "lic".
    * Enter an item that starts with "Gua" and ends with "la".
    * Enter an item that starts with "Guer".
    * Enter an item that starts with "Rus".

    ## Utterance fields

    * end
    * start

    ## Custom settings

    None
    """

    subdomain = "use-autocomplete"


class UseAutocompleteNodelayEnv(MiniWoBEnvironment):
    """
    ## Description

    [use-autocomplete]

    ## Example utterances

    * Enter an item that starts with "An" and ends with "ica".
    * Enter an item that starts with "Ce" and ends with "lic".
    * Enter an item that starts with "Gua" and ends with "la".
    * Enter an item that starts with "Guer".
    * Enter an item that starts with "Rus".

    ## Utterance fields

    * end
    * start

    ## Custom settings

    None
    """

    subdomain = "use-autocomplete-nodelay"


class UseColorwheelEnv(MiniWoBEnvironment):
    """
    ## Description

    Use a color wheel.

    ## Example utterances

    * Select black with the color picker and hit Submit.
    * Select blue with the color picker and hit Submit.
    * Select gold with the color picker and hit Submit.
    * Select maroon with the color picker and hit Submit.
    * Select yellow with the color picker and hit Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "use-colorwheel"


class UseColorwheel2Env(MiniWoBEnvironment):
    """
    ## Description

    Use a color wheel given specific random color.

    ## Example utterances

    * Select the following color with the color picker and hit Submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "use-colorwheel-2"


class UseSliderEnv(MiniWoBEnvironment):
    """
    ## Description

    Use a slider to select a particular value.

    ## Example utterances

    * Select -97 with the slider and hit Submit.
    * Select -99 with the slider and hit Submit.
    * Select 0 with the slider and hit Submit.
    * Select 129 with the slider and hit Submit.
    * Select 47 with the slider and hit Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "use-slider"


class UseSlider2Env(MiniWoBEnvironment):
    """
    ## Description

    Use sliders to create a given combination.

    ## Example utterances

    * Set the sliders to the combination [11,19,5] and submit.
    * Set the sliders to the combination [12,3,11] and submit.
    * Set the sliders to the combination [17,10,11] and submit.
    * Set the sliders to the combination [19,5,9] and submit.
    * Set the sliders to the combination [6,6,0] and submit.

    ## Utterance fields

    * n1
    * n2
    * n3

    ## Custom settings

    None
    """

    subdomain = "use-slider-2"


class UseSpinnerEnv(MiniWoBEnvironment):
    """
    ## Description

    Use a spinner to select given number.

    ## Example utterances

    * Select -10 with the spinner and hit Submit.
    * Select -3 with the spinner and hit Submit.
    * Select -7 with the spinner and hit Submit.
    * Select 5 with the spinner and hit Submit.
    * Select 7 with the spinner and hit Submit.

    ## Utterance fields

    * target

    ## Custom settings

    None
    """

    subdomain = "use-spinner"


class VisualAdditionEnv(MiniWoBEnvironment):
    """
    ## Description

    Count the total number of blocks.

    ## Example utterances

    * Type the total number of blocks into the textbox and press Submit.

    ## Utterance fields

    (none)

    ## Custom settings

    None
    """

    subdomain = "visual-addition"
