from django import forms
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
