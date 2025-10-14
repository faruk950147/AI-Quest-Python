from django import forms
from django import forms


"""
  | **Parameter**    | **Description**                                       | **Example**                                                                  |
| ---------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| `label`          | Display name for the field                            | `name = forms.CharField(label='Full Name')`                                  |
| `label_suffix`   | Text shown after the label (like `:` or a space)      | `name = forms.CharField(label='Name', label_suffix=':')`                     |
| `initial`        | Default value for the field                           | `roll = forms.IntegerField(initial=101)`                                     |
| `required`       | Specifies whether input is mandatory (default = True) | `email = forms.EmailField(required=False)`                                   |
| `help_text`      | Small help message displayed below the field          | `age = forms.IntegerField(help_text='Enter your age in years')`              |
| `widget`         | Custom HTML input type or attributes                  | `dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))`      |
| `min_value`      | Minimum allowed numeric value                         | `age = forms.IntegerField(min_value=18)`                                     |
| `max_value`      | Maximum allowed numeric value                         | `age = forms.IntegerField(max_value=100)`                                    |
| `min_length`     | Minimum allowed text length                           | `username = forms.CharField(min_length=3)`                                   |
| `max_length`     | Maximum allowed text length                           | `username = forms.CharField(max_length=30)`                                  |
| `choices`        | Defines dropdown/select options                       | `gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])`       |
| `disabled`       | Makes the field read-only (non-editable)              | `name = forms.CharField(initial='Faruk', disabled=True)`                     |
| `error_messages` | Custom error messages for validation errors           | `roll = forms.IntegerField(error_messages={'required': 'Roll is required'})` |
| `validators`     | Adds custom validation functions                      | `email = forms.EmailField(validators=[validate_email])`                      
| `auto_id`       | Automatically generates an `id` attribute for the field | `name = forms.CharField(auto_id='name_field')`                              |   
| `order
  
"""

class Registration(forms.Form):
    name = forms.CharField(
        label='Name', initial='Faruk', max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )

    roll = forms.IntegerField(
        label='Roll',
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your roll number'})
    )

    dob = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(
            attrs={'type': 'date', 
            'class': 'form-control',
            'placeholder': 'Select your date of birth'})
    )

    
    department = forms.ChoiceField(
        choices=[
            ('CSE', 'Computer Science'),
            ('EEE', 'Electrical Engineering'),
            ('ME', 'Mechanical')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    agree = forms.BooleanField(
        label='I agree to the terms', initial=False, required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # as your wish
        self.order_fields(['roll', 'name', 'email', 'department', 'dob', 'agree'])




