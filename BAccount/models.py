from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .utilities import send_activation_notification

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Фаоллаштирилдими?')
    send_messages = models.BooleanField(default=True, verbose_name='Хабар юбориш мумкинми?')
    owner_company_id = models.ForeignKey('OwnerCompany', on_delete=models.CASCADE,
                                         verbose_name='Қайси ташкилот',
                                         default=0)

    class Meta(AbstractUser.Meta):
        verbose_name = 'Фойдаланувчи'
        verbose_name_plural = 'Фойдаланувчилар'


# owner company
class OwnerCompany(models.Model):
    name = models.CharField('Компания номи', max_length=150)
    short_name = models.CharField('Қисқа номи', max_length=50)
    code = models.IntegerField('Коди', unique=True)
    date_activate = models.DateTimeField('Рўйхатдан ўтган санаси ва вақти', auto_now=True)
    date_deactivate = models.DateTimeField('Фойдаланиш тўхтаган сана, вақти', null=True)
    status = models.IntegerField('Шартнома холати')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сайтда хисобини юритувчи'
        verbose_name_plural = 'Сайтда хисобини юритувчи'
        ordering = ['-name']
        db_table = 'owner_company'


# Create your models here.
# Пуллар-Тўлов турлари
class ListCurrency(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', on_delete=models.CASCADE, verbose_name='Ташкилот')
    code = models.IntegerField(verbose_name='Код', unique=True)
    name = models.CharField(max_length=50, verbose_name='Валюта номи')
    short_name = models.CharField(max_length=10, verbose_name='Қисқа номи')
    currency_symbol = models.CharField(max_length=5, verbose_name='Валюта символи')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тўлов тури'
        verbose_name_plural = 'Тўлов турлари'
        ordering = ['-name']
        db_table = 'list_currency'


# Қолдиқни хисоблаш усули
class ListBalanceCalcMethod(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', on_delete=models.CASCADE, verbose_name='Ташкилот')
    code = models.IntegerField(verbose_name="Код")
    name = models.CharField(verbose_name="Номи", max_length=50)
    description = models.CharField(verbose_name="Изох", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Қолдиқни хисоблаш усули'
        verbose_name_plural = 'Қолдиқни хисоблаш усуллари'
        ordering = ['-name']
        db_table = 'list_balance_calc_method'


# Товарлар
class ListGood(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', on_delete=models.CASCADE, verbose_name='Ташкилот')
    code = models.IntegerField(verbose_name='Код', unique=True)
    name = models.CharField(verbose_name='Товар номи', max_length=100)
    unit_measurement_main = models.CharField(verbose_name='Йирик ўлчови', max_length=25)
    unit_measurement_small = models.CharField(verbose_name='Кичик ўлчови', max_length=25)
    balanceCalcMethod = models.ForeignKey('ListBalanceCalcMethod', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товарлар'
        ordering = ['-name']
        db_table = 'list_good'


# Good Partition
class GoodPartition(models.Model):
    company_id = models.ForeignKey('OwnerCompany', on_delete=models.CASCADE, verbose_name='Ташкилот')
    good_id = models.ForeignKey('ListGood', on_delete=models.CASCADE, verbose_name='Товар')
    accept_date = models.DateField('Қабул қилинган сана')
    purchase_price = models.DecimalField('Олиш нархи', max_digits=18, decimal_places=2)
    selling_price = models.DecimalField('Олиш нархи', max_digits=18, decimal_places=2)
    quantity_per_pack = models.DecimalField('Катта ўлчам ичида майда ўлчамдагисининг сони', max_digits=18,
                                            decimal_places=2)
    purchased_from = models.ForeignKey('ListCustomer', on_delete=models.CASCADE,
                                       verbose_name='Бу товар партияси кимдан олинган')

    def __str__(self):
        return str(self.company_id) + '/' + str(self.good_id) + '/' + str(self.id)

    class Meta:
        verbose_name = 'Товар партияси'
        verbose_name_plural = 'Товар партиялари'
        db_table = 'good_partition'


# Мижозлар
class ListCustomer(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', on_delete=models.CASCADE, verbose_name='Ташкилот')
    code = models.IntegerField("Номери", unique=True)
    name = models.CharField("Номи", max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ҳамкор'
        verbose_name_plural = 'Хамкорлар'
        ordering = ['-name']
        db_table = 'list_customer'


# ходимлар
class ListEmployee(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', on_delete=models.CASCADE, verbose_name='Ташкилот')
    name = models.CharField('Исми шарифи', max_length=50)
    salary = models.DecimalField('Ойлик иш хақи', max_digits=18, decimal_places=2)
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Фаолми?')
    enrollment_date = models.DateField('Ишга кирган санаси')
    date_of_dismissal = models.DateField('Ишдан бўшаган сана')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ташкилот ходими'
        verbose_name_plural = 'Ташкилот ходимлари'
        db_table = 'list_employee'


# "Касса-Терминал-Хисоб/рақам"- пул маблағларини қолидиғини сақлаш
class CashBox(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', verbose_name='Ташкилот', on_delete=models.CASCADE)
    currency_id = models.ForeignKey('ListCurrency', verbose_name='Пул тури', on_delete=models.CASCADE)
    work_day = models.DateField('Иш куни')
    accepted = models.DecimalField('Қабул қилинди(бир кунда)', max_digits=18, decimal_places=2)
    issued = models.DecimalField('Берилди(бир кунда)', max_digits=18, decimal_places=2)
    remaining = models.DecimalField('Кун охирига қолди', max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = 'Пул маблағи'
        verbose_name_plural = 'Пул маблағлари'
        db_table = 'cash_box'


# Товар қолдиқлари
class GoodTurnoverRemaining(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', verbose_name='Ташкилот', on_delete=models.CASCADE)
    good_partition_id = models.ForeignKey('GoodPartition', verbose_name='Товар партияси', on_delete=models.CASCADE)
    work_day = models.DateField('Иш куни')
    accepted = models.DecimalField('Қабул қилинди(бир кунда)', max_digits=18, decimal_places=2)
    issued = models.DecimalField('Берилди(бир кунда)', max_digits=18, decimal_places=2)
    remaining = models.DecimalField('Кун охирига қолди', max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = 'Товар қолдиғи'
        verbose_name_plural = 'Товар қолдиқлари'
        db_table = 'good_turnover_remaining'


# Хамкорлар қолдиқлари
class EmployeeTurnoverRemaining(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', verbose_name='Ташкилот', on_delete=models.CASCADE)
    employee_id = models.ForeignKey('ListEmployee', verbose_name='Ходим', on_delete=models.CASCADE)
    work_day = models.DateField('Иш куни')
    accepted = models.DecimalField('Хақдор бўлди(бир кунда)', max_digits=18, decimal_places=2)
    issued = models.DecimalField('Хақи камайди(бир кунда)', max_digits=18, decimal_places=2)
    remaining = models.DecimalField('Кун охирига қолган хақи ёки қарзи', max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = 'Ходим хақи ўзгариши'
        verbose_name_plural = 'Ходим хақи ўзгариши'
        db_table = 'employee_turnover_remaining'


# Тўлов турлари
class ListPaymentType(models.Model):
    owner_id = models.ForeignKey('OwnerCompany', verbose_name='Ташкилот', on_delete=models.CASCADE)
    code = models.IntegerField('Код', unique=True, null=False)
    currency_id = models.ForeignKey('ListCurrency', verbose_name='Пул тури', on_delete=models.CASCADE)
    name = models.CharField('Номи', max_length=200)
    direction_accepted = models.BooleanField('Пул кирим қилиняптими(кассага)', default=True)
    can_user_select = models.BooleanField('Танлаш мумкинми', default=False)

    class Meta:
        verbose_name = 'Тўлов тури'
        verbose_name_plural = 'Тўлов турлари'
        db_table = 'list_payment_type'

    def __str__(self):
        return str(self.owner_id) + '/' + str(self.code) + '/' + self.name
