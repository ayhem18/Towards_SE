import uuid

from django.db import models
from django.urls import reverse

from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower # Returns lower cased value of field


# let's build some models
class Genre(models.Model):
    name = models.TextField(max_length=50, unique=True)

    def __str__(self):
        # the name will be used the string
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'), # when a new genre record is added to the database, it has to be unique. It cannot be one of already existing records
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]


class Language(models.Model):
    # this code is mainly inspired from the Django documentation: 
    # https://docs.djangoproject.com/en/5.1/ref/models/fields/ 

    # create a inner class with all the different choices
    class _lang(models.TextChoices):
        ENG = "ENG", _("English")  # not really sure what is happening here !!!
        FRE = "FRE", _("French")
        SP = "SP", _("Spanish")
        GER = "GER", _("German")
        RUS = "RUS", _("Russian")
        KOR = "KOR", _("Korean")

    lanuage = models.CharField(max_length=3, choices=_lang)

    def __str__(self) -> str:
        return self._lang[self.lanuage]


class Author(models.Model):
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)

    date_of_birth = models.DateField()
    # some stack overflow suggests setting blank=True too, 
    # https://stackoverflow.com/questions/16828315/how-can-i-make-my-model-fields-optional-in-django 
    # not sure about that though...
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    
    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])


class Book(models.Model):
    title = models.TextField(max_length=150, )
    author = Author
    summary = models.TextField(max_length=1000)
    isbn = models.TextField(max_length=100,     primary_key=True)
    
    genres = models.ManyToManyField(Genre, help_text='set the book genres')

    author = models.ForeignKey(Author, 
                               on_delete=models.RESTRICT # no author can be deleted if at least on of their books are saved in the catalog
                               )

    def __str__(self) -> str:
        f'{self.title} written by {self.author.first_name} {self.author.last_name}'        
        return super().__str__()



class BookInstance(models.Model):
    class _loan_status(models.TextChoices):
        _M = "M", _('Maintenance')
        _O = "O", _('On loan')
        _A = "A", _('Available')
        _R = "R", _('Reserved')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")    

    book = models.ForeignKey(Book,
                             on_delete=models.RESTRICT
                             )
    
    status = models.TextField(choices=_loan_status, 
                              max_length=len(_loan_status._M))
    
    due_back = models.DateField(null=True, blank=True, # null when the book is not used
        help_text="The date when the model should be returned to the library's storage")
    
   
    class Meta:
        # this field determines the order of items returned when querying the dataset
        ordering = ['due_back']    
