from django.db import models
from django.contrib.auth.models import User
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import encodestring, decodestring
from django.db import models
from Crypto import Random
from django.utils.text import slugify
from Crypto.Cipher import AES
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.



#model for cards
class cards(models.Model):
	title = models.CharField(max_length=200)
	card_no=models.CharField(max_length=30)
	card_name=models.CharField(max_length=30)
	card_expiry=models.DateField()
	owner=models.ForeignKey(User,on_delete=models.CASCADE)
	slug = models.SlugField(max_length=10, unique=True)

	def __str__(self):
		return self.card_name

	def cardis(self):
		return self.card_name+" "+self.card_no[:4]+"XXXXXXXX"

	def _get_unique_slug(self):
		slug=slugify(self.title)
		unique_slug=slug
		num=1
		while cards.objects.filter(slug=unique_slug).exists():
			unique_slug= '{}-{}'.format(slug,num)
			num+=1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug=self._get_unique_slug()
		super().save(*args,**kwargs)

class Entry(models.Model):

    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=10, unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    nonce=models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Entry.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

#crypto engine
class CryptoEngine:

    PADDING = '{'
    BLOCK_SIZE = 32
    # TODO: use the random bit string as salt
    IV = Random.new().read(AES.block_size)

    def __init__(self, master_key):

        self.master_key = master_key
        key=key = b'456789abcdefghijklmnopqrstuvwxyz'
       # self.secret = self._get_secret(master_key)
       # self.cipher = AES.new(self.secret)
       # self.decipher = AES.new(self.secret)
        self.cipher = AES.new(key, AES.MODE_CBC, self.IV)
        self.decipher = AES.new(key, AES.MODE_CBC,self.IV)

    def _pad(self, msg, block_size=BLOCK_SIZE, padding=PADDING):
        return msg + ((block_size - len(msg) % block_size) * padding)

    def _depad(self, msg, padding=PADDING):
        return msg.rstrip(padding)

    def _get_secret(self, key):
        return MD5.new(key).hexdigest()[:self.BLOCK_SIZE]

    def encrypt(self, msg):
        return encodestring(self.cipher.encrypt(self._pad(msg).encode("utf8")))

    def decrypt(self, msg):
        return self._depad((self.decipher.decrypt(decodestring(msg))))


#meeting model
class Meetings(models.Model):
    title = models.CharField(max_length=200)
    meeting_id = models.CharField(max_length=200)
    meeting_with = models.CharField(max_length=200)
    meeting_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=10, unique=True)

    def __str__(self):
        return self.title
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Entry.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)