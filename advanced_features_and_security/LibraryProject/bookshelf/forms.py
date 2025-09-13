from django import forms
from django.core.validators import RegexValidator
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for creating and editing Book instances.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': '1000',
                'max': '2100'
            }),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author',
            'publication_year': 'Publication Year',
        }
        help_texts = {
            'title': 'Enter the full title of the book',
            'author': 'Enter the author\'s full name',
            'publication_year': 'Enter the year the book was first published',
        }
    
    def clean_publication_year(self):
        """
        Validate publication year.
        """
        year = self.cleaned_data.get('publication_year')
        if year and (year < 1000 or year > 2100):
            raise forms.ValidationError('Publication year must be between 1000 and 2100.')
        return year
    
    def clean_title(self):
        """
        Validate and clean title.
        """
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 2:
                raise forms.ValidationError('Title must be at least 2 characters long.')
        return title


class SecureSearchForm(forms.Form):
    """
    Secure search form with proper validation.
    """
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter search term...',
            'maxlength': '100'
        }),
        help_text='Maximum 100 characters'
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('title', 'Title'),
            ('author', 'Author'),
            ('both', 'Both'),
        ],
        initial='both',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean_search_query(self):
        """
        Security: Validate and sanitize search query.
        """
        search_query = self.cleaned_data.get('search_query', '').strip()
        
        # Security: Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`', '$']
        for char in dangerous_chars:
            if char in search_query:
                raise forms.ValidationError(f'Search query contains invalid character: {char}')
        
        # Security: Check for SQL injection patterns
        sql_patterns = ['union', 'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter']
        search_lower = search_query.lower()
        for pattern in sql_patterns:
            if pattern in search_lower:
                raise forms.ValidationError('Search query contains invalid content.')
        
        return search_query


class ContactForm(forms.Form):
    """
    Secure contact form with comprehensive validation.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'maxlength': '100'
        }),
        help_text='Your full name (maximum 100 characters)'
    )
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'maxlength': '254'
        }),
        help_text='Your email address'
    )
    
    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message...',
            'rows': 4,
            'maxlength': '1000'
        }),
        help_text='Your message (maximum 1000 characters)'
    )
    
    def clean_name(self):
        """
        Security: Validate name field.
        """
        name = self.cleaned_data.get('name', '').strip()
        
        # Security: Check for minimum length
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        
        # Security: Check for valid characters (letters, spaces, hyphens, apostrophes)
        name_validator = RegexValidator(
            regex=r'^[a-zA-Z\s\-\']+$',
            message='Name can only contain letters, spaces, hyphens, and apostrophes.'
        )
        name_validator(name)
        
        return name
    
    def clean_message(self):
        """
        Security: Validate message field.
        """
        message = self.cleaned_data.get('message', '').strip()
        
        # Security: Check for minimum length
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        
        # Security: Check for potentially dangerous content
        dangerous_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
        message_lower = message.lower()
        for pattern in dangerous_patterns:
            if pattern in message_lower:
                raise forms.ValidationError('Message contains invalid content.')
        
        return message
