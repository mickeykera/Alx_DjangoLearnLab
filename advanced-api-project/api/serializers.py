from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization and deserialization of Book instances.
    
    This serializer includes all fields from the Book model and implements
    custom validation to ensure the publication_year is not in the future.
    The serializer also handles the foreign key relationship with Author.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization and deserialization of Author instances.
    
    This serializer includes the author's name and uses a nested BookSerializer
    to serialize all related books. The nested relationship allows for complete
    author data including their books to be serialized in a single response.
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        """
        Custom representation method to handle the nested book serialization.
        
        This method ensures that when an Author is serialized, all related
        books are included in the response using the BookSerializer.
        """
        data = super().to_representation(instance)
        # The books field is automatically handled by the nested BookSerializer
        return data
