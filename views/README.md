# Structure of the GUI
For Reference click the [GUI flow](https://drive.google.com/file/d/1-EQPn6qUzVsC2B4StnYKVexv7ps9LH9F/view?usp=sharing)

## Branch Current Version is 1.0.8

### Doing
> 1. Admin Page and other Aspect Ratio Fixes

### To Do

General To Do:
> 1. Integrate The functions from Controller.py to GUI.
> 2. Database Connection.
> 3. Forget Password Page
> 4. Change Global Theme

Specific To Do **(Login)**:
> 1. Input Validation.
> 2. Warning whenever an incorrect ID/Password is entered.
> 3. Create a function for loginButton that verifies the password and ID before parent.show_frame(parent.dashboardFrame).
> 4. Ensure that inputs to text field would impact the database.

Specific To do **(Dashboard)**:
> 1. Auto populate the Database Treeview.
> 2. Add buttons for updating, deleting table entries based on requirements.
> 3. Specify the limit of entries visible to the Treeview.
> 4. Ideally, the treeview is just a display, it's not supposed to be interactive, and it will not affect the database.
> 5. Add the camera change functionality.
> 6. Must show real-time vehicles detected by the said camera.
> 7. Must show the up-time of the algorithm.
> 8. Must show the camera ID of the current Camera displayed.
> 9. Must show the live detection feed of vehicles in the Camera Placeholder.
> 10. Admin Button must be disabled if the access level of the user is insufficient.

Specific To Do **(Config)**:
> 1. Input validation for Active Hours.
> 2. Modify the addRow function to validate the row first if the time and day is valid before adding another row.
> 3. When the Config Page is loaded, the saved values for the Active Hours must be visible from the start. For example, if I have previously set ***From 6 AM To 8 AM Every Mondays***, if I click the Settings button from the Dashboard Page, the **first row of the Active Hours** should be ***From 6 AM To 8 AM Every Mondays***.
> 4. In Detectable Vehicles, same with the Active Hours, the saved configuration must be loaded once the Config Page is called. If I have previously set the Car to be disabled, the car should still be disabled once I click the Settings button from the Dashboard Page.
> 5. In Congestion Price, the saved configuration must also be either the placeholder or current text value of the entries once I clicked the Settings Button from the Dashboard Page.
> 6. Change Theme is also the same, configuration must be saved and still be the same when reopening the Config Page.
> 7. Change Theme System Default means the Light or dark mode of the application is based on the current system's settings for theme.
> 8. Change Password must have Input Valdiation.
> 9. Change Password must not affect the Database.
> 10. An appropriate feedback must be returned to the user if the password does not match or incorrect Old Password.
> 11. Once I click the save button of the Change Password, the text field must be cleared.
> 12. Apply Now Button must apply immediately the changes in the Active Hours, Detectable Vehicles, and Congestion Price. While the Change Theme is applied immediately after selecting a radio button and not included in the Apply button or scheduled Apply button.
> 13. Scheduled Apply button must not be based on the system's time. But use an API that pulls the current time of the PHT or +8:00 Timezone and compares if the current time is equal to the Scheduled Apply.
> 14. Layout for Scheduled Apply. Preferrably a popup.
> 15. Logout Button must have a confirmation popup first.

Specific To Do **(Admin)**:
> 1. Define the Requirements.
> 2. Build the GUI.

Specific To Do **(Analytics)**:
> 1. Define the Requirements.
> 2. Build the GUI.

Specific To Do **(Forget Password)**:
> 1. Define the Requirements.
> 2. Build the GUI.

Specific To Do **(Error Feedback)**:
> 1. Define the Requirements.
> 2. Build the GUI.