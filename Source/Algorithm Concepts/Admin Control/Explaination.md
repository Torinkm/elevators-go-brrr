# Starting the Program
MaxIndex is initialised with the intager value 10

A new variable is initialised called CurrentIndex whis is set to the intager 0

A new aray called CurrentProducts is initialized as an array with the Value of MaxIndexd [10] being how many free slots are given [in this case 10 slots, from 0 to 9]

The MaxIndex is then set to the last value it had, minus 1 [going from 10, to 9]

In an actual program, the amount of spaces in CurrentProducts should be infinate,
but due to restrictions in flowgorithm, it is set to 10 spaces

A New variable is initialized called Index which will be used in a counter-controlled loop.
This iteration will set every spot of the array to a blank string to avoid errors with flowgorithm later on.
[This can be avoided in most coding languages but it can be restrictive in flowgirothm].

Next a new variable called IsAdmin is initialized, which can take boolean data [true, false] which it then stores, in the actual code itself,
admins are determined by their username, and should be set beforehand, without an input being sent to the user if they are an admin

# When IsAdmin == false
The program will end, as the user is not an admin, and therefore cannot edit what is avaliable.
# When IsAdmin == true
A variable called Option is Initialized with the option 0 to ensure the condition controlled loop responsible
for asking for the option is ran.

The User is given 4 options to choose from. They need to type 1-4 depending on what option they want, and should be asked for the option they want if they
do not type the correct range of intagers.

Option is then checked to see if it is between 1 and 4.

# If Option 1 is chosen [Option == 1]
This Option is for adding content to the CurrentProducts array

A Variable called NewProduct is initialized and is set to be a blank string value [""]

The boolean variables, FoundLostIndex and Error, are initialized both with a value of false

The variable Index has it's value changed to the intager 0

A counter controled loop will run, checking if Error is false, FoundLostIndex is false, and that Index is not set to the intager 10.
if tthe condition is met, It will check the CurrentProducts array at the index of the value set as Index to see if it is blank,
if so, it will change FoundLostIndex's value to true and the condition is tested again. Else, the index will be incremented by 1, and it will see if the index is
greater than MaxIndex, if so, the variable Error has it's value changed to true, else nothing will happen, and the condition is checked again.

When the condition is no longer met, it will check if an error occured [when the Index value is larger than the MaxIndex value],
if so the program assumes the array is full, and will return a controlled error message saying the array is full, else, it will check if the value in
NewProduct is a string with no value in it. When coding this, you should strip any excess formatting or spaces from the value in NewProduct before passing it through the if statement, because the user may be able to input a blank value into the array

The program will then ask the user if they want to choose another option

# If Option 2 is chosen [Option == 2]
Option 2 should allow the user to edit or change data related to the Product [like product name]

The program will first output the title "Current Products:" to the user

The variable OptionCount is initialized and given the value of the intager 0

The program should then use a counter controled loop to iterate over each value of the array CurrentProducts where it will then check if the spaqce has a
value or a blank string. If there is a value, OptionCount should increment by 1, else nothing will happen and the iteration should check the next value.

Once the counter controlled loop is finished, the value of OptionCount is then examined to see if it is larger than 0, its base value.

If OptionCount's value is 0, the program should state that there is no data to be edited, before looping back to ask the User t select a different option.
However, if OptionCount's value is over 0, GetIndex is initialized with the value of the intager -10 and NewProduct is initialized with a base string value [""]

A condition controlled loop is then ran, checking if GetIndex is in the range of 0, to the value of MaxIndex.
If the value is not in the range, the program should ask for a new value for GetIndex, in which it should be checked to see if it is an intager before 
being set as the new value of GetIndex, else the value will be set as an invalid [probably back to -10] in which the condition is checked again.

Once the user has inputted a suitible valuefor GetIndex, the user is then asked for the naqme of the new product, in which their input, as a string, 
should be set as the new value of NewProduct.

Then the new value of NewProduct should be checked if it is blank or not [using the same code to strip the value of formatting and unecessary spaces].
If the value of NewProduct is blank [aka = ""], the program should not comit the edit, however if a new name for the product is added, the name shoudl be replaced with the
inputted name from the user.

The code will then loop all the way back to the user being asked for an option again.

# If Option 3 is chosen [Option == 3]

Option 3 deals with deleting data from the list if any data exists, this allows any products that may be out of stock
or even no longer avaliable to hire due to maintinence, or lack of support.

The program will first output "Please select Which data yu would like to remove"

Then the program initializes a new variable called Option count, in which its value is assinged to the intager 0

then a counter controlled loop is run, where the previously declared Index will now iterate between the values of 0 to 9whatever the value of MaxdIndex is. During this iteration, the program should check if the valueis a blank string [potentiallyu using a strip on the value. If the value is not blank, it will list is as an option with the indexd number as well as the data inside, and will increment Option count by 1, else nothing will happen.

Once the counter controlled iteration finishes, it checks if the value of OptionCount is greater than 0, if it is 0, it will output that "No products were found" and return the user back to selecting an option, ese if it is greater than 0, it initializes an intager variable called SelectedNumber which will be assigned the integer value of -5.

A condition controlled loop will then run, checking if the Selected Number is out of the range of 0 to the value of MaxIndex [9 in this example], t it is out of the range, it will ask the user to input what item they want to delete, and will ask for an integer input from the user. Once the Number is in the range, the number inputted is looked for in the array CurrentProducts and is replaced with a blank string value [""].

And finallly, the user is taken back to the starting point where they get to select an option again.

# If Option 4 is chosen [Option == 4]
Nothing will run, however the requirement for the condition controlled loop for the Option not being for will no longer be met, causing the program to end

# If an option is not chosen [Option != 4 / else]
Nothing will run, and the User will be asked again for an option, hopefully with an error message saying the option should be in range of 1 to 4.

