from django.shortcuts import render
from lab.models import *

cart_id = [{
    "customer_address": "Москва ул. Иваново стр. 23/3",
    "customer_phone": "8 880 554 54 54",
    "items": [{
        "item_id": 1,
        "count": 12
    }, {
        "item_id": 5,
        "count": 3
    }, {
        "item_id": 8,
        "count": 1
    }],
},]
data = [
        {'name': 'автоматичекий аппарат для определения температуры помутнения нефтепродуктов', 'description': 'Автоматический аппарат АТП-ЛАБ-12 предназначен для определения температуры помутнения нефтепродуктов в строгом соответствии со стандартами DIN EN 23015, ISO 3015, ASTM D2500. Конструкция аппарата и метод проведения анализа полностью выполняет все требования стандартов DIN EN 23015, ISO 3015, ASTM D2500. Аппарат АТП-ЛАБ-12 сочетает в себе последние достижения в области разработки автоматического лабораторного оборудования и выгодно отличается от конкурентов наличием встроенного холодильного модуля, компактными размерами, открытым программным обеспечением и прост в управлении и использовании.', 'price': 1000, 'id': 0, 'image': 'http://localhost:9000/lab1/automatic_apparatus_for_determining_the_turbidity_temperature_of_petroleum.jpg'},
{'name': 'автоматический аппарат для определения фракционного состава нефти и нефтепродуктов', 'description': 'Автоматический аппарат АРН-ЛАБ-11 предназначен для определения фракционного состава светлых и темных нефтепродуктов при атмосферном давлении в соответствии с ГОСТ Р ЕН ИСО 3405, ГОСТ ISO 3405, ГОСТ 2177-99 (метода А и Б), ГОСТ P 53707, ASTM D86, ISO 3405, IP123 и другими аналогичными стандартами в диапазоне температур до 450°С. На основании положительных результатов межлабораторных сравнительных испытаний, рекомендован техническим комитетом по стандартизации ТК-31 к применению для определения фракционного состава нефтепродуктов.', 'price': 2000, 'id': 1, 'image': 'http://localhost:9000/lab1/products_automatic_apparatus_for_determining_the_fractional_composition_of_oil_and_petroleum.jpg'},
{'name': 'аквадистиллятор автоматический', 'description': 'Автоматический аквадистиллятор LOIP LD-104 предназначен для получения дистиллята высокого качества методом однократной дистилляции. Простой и надежный в эксплуатации аппарат, обеспечивающий лабораторию требуемым количеством дистиллята, в автоматическом режиме.', 'price': 3000, 'id': 2, 'image': 'http://localhost:9000/lab1/products_aquadistillator_automatic.jpg'},
{'name': 'баня водяная четырёхместная', 'description': 'Водяная баня LOIP LB-140 применима для задач, не требующих высокой точности поддержания температуры. Простая и надежная в эксплуатации модель LOIP LB-140 оснащена цифровым регулятором температуры со светодиодным дисплеем, а также системой защиты от перегрева.', 'price': 4000, 'id': 3, 'image': 'http://localhost:9000/lab1/water_bath_four.jpg'},
{'name': 'баня водяная шестиместная', 'description': 'Водяная баня LOIP LB-160 применима для задач, не требующих высокой точности поддержания температуры. Простая и надежная в эксплуатации модель LOIP LB-160 оснащена цифровым регулятором температуры со светодиодным дисплеем, а также системой защиты от перегрева.', 'price': 5000, 'id': 4, 'image': 'http://localhost:9000/lab1/water_bath_six.jpg'},
{'name': 'колбонагреватель', 'description': 'Колбонагреватели для круглодонных колб LOIP LH-200 применяются для нагрева жидкостей и твердых веществ, проведения синтеза и перегонки, контроля фракционного состава, определения содержания воды по действующим стандартам и других задач, предусматривающих нагревание при температурах до +600°С. Модель LOIP LH-225 предназначена для нагрева круглодонных колб объемом от 50 до 250 мл.', 'price': 6000, 'id': 5, 'image': 'http://localhost:9000/lab1/flask_heater.jpg'},
{'name': 'криотермостат жидкостный', 'description': 'Предназначен для термостатирования образов как в собственной ванне, так и во внешних системах замкнутого типа, в диапазоне температур от -25 °С до +100 °С.', 'price': 7000, 'id': 6, 'image': 'http://localhost:9000/lab1/cryothermostat_liquid.jpg'},
{'name': 'печь трубчатая', 'description': 'Печь трубчатая LOIP LF-50/500-1200 предназначена для проведения физико-химических анализов и исследований, термообработки (нагрев, закалка, обжиг) различных материалов в воздушной среде при температурах от +300°С до +1200°С', 'price': 1000, 'id': 7, 'image': 'http://localhost:9000/lab1/furnace_tubular.jpg'},
{'name': 'печь муфельная', 'description': 'Лабораторная муфельная печь для подготовки проб в химическом анализе, проведения нагрева, закалки и обжига материалов в воздушной среде при температурах до +1300°С.', 'price': 1000, 'id': 8, 'image': 'http://localhost:9000/lab1/furnace_muffle.jpg'},
{'name': 'плита нагревательная', 'description': 'Нагревательная плита LOIP LH-302 с рабочей поверхностью из стеклокерамики предназначена для безопасного нагрева одновременно нескольких проб в одинаковых условиях. Благодаря высокой химической стойкости материала рабочей поверхности, прибор можно применять для нагрева самых агрессивных реагентов (концентрированных кислот и щелочей) без риска коррозии нагревательной поверхности.', 'price': 1000, 'id': 9, 'image': 'http://localhost:9000/lab1/plate_heating.jpg'},
{'name': 'термостаи циркуляционный', 'description': 'Экономичные термостаты семейства LOIP LT-100 предназначены для поддержания заданной температуры объектов в ванне, а также для термостатирования внешних систем: лабораторных реакторов, измерительных ячеек рефрактометров, вискозиметров, электрохимических анализаторов и т.п. Прибор модификации LOIP LT-112a состоит из погружного термостата-циркулятора LOIP LT-100 и рабочей ванны с плоской съемной крышкой.', 'price': 1000, 'id': 10, 'image': 'http://localhost:9000/lab1/thermostat_circulation.jpg'},
{'name': 'устройство подъёмаопускания обазцов', 'description': 'Устройство подъема-опускания образцов к термостатам и термобаням с ванной объёмом 12 и 16 л. \n Предназначено для погружения объектов в ванны термостатов LOIP LT и прецизионных термостатирующих бань LOIP LB-200 на заданную глубину. Термостатируемые объекты размещают на передвижном поддоне, который может быть зафиксирован на любой требуемой глубине. Устройство устанавливается на кожух термостатов и прецизионных термостатирующих бань вместо откидной крышки и комплектуется собственной съемной крышкой.', 'price': 1000, 'id': 11, 'image': 'http://localhost:9000/lab1/device_for_lifting_and_lowering_the_rim.jpg'},
{'name': 'шейкер орбитальный', 'description': 'Универсальный орбитальный шейкер LOIP LS-110 с аналоговым управлением применяется для перемешивания и нагрева (до +100 °С) в колбах, делительных воронках и других сосудах.', 'price': 1000, 'id': 12, 'image': 'http://localhost:9000/lab1/shaker_orbital.jpg'},
{'name': 'шкаф сушильный', 'description': 'Лабораторный сушильный шкаф для нагрева, высушивания и тепловой обработки различных материалов в воздушной среде при температурах до +350°С.', 'price': 1000, 'id': 13, 'image': 'http://localhost:9000/lab1/drying_cabinet.jpg'},
{'name': 'штатив для пробирок', 'description': 'Штатив из нержавеющей стали для размещения пробирок диаметром 20 мм в криостатах LOIP FT и термостатах LOIP LT с ваннами на 11 л.', 'price': 1000, 'id': 14, 'image': 'http://localhost:9000/lab1/tripod_for_test_tubes.jpg'}
    ]

def GetLaboratoryCatalog(request):
    print(LaboratoryItem.objects.all())
    product_price = request.GET.get("laboratory-price")
    if product_price != None:
        return render(request, 'laboratory_catalog.html', {
            'data': LaboratoryItem.objects.filter(price__lte = int(product_price)),
            'searched_price': product_price,
            'cart': LaboratoryOrderItems.objects.filter(order=1).count()
        })
    return render(request, 'laboratory_catalog.html', {
        'data': LaboratoryItem.objects.all(),
        'cart': LaboratoryOrderItems.objects.filter(order=1).count()
    })


def GetLaboratoryItemInformation(request, selected_id):
    return render(request, 'laboratory_item_information.html', {
        'data': LaboratoryItem.objects.filter(id=selected_id),
        'cart': LaboratoryOrderItems.objects.filter(order=1).count()})
# Create your views here.

def GetLaboratoryCart(request, id):
    a = LaboratoryItem.objects.filter(laboratoryorderitems__order=1)
    final_price = 0
    for i in a:
        final_price += 1
        #final_price += i['price']
    return render(request, 'laboratory_cart.html', {
        'data': LaboratoryItem.objects.filter(laboratoryorderitems__order=1),
        'final_price': final_price
    })

def AddLaboratoryItem(request, selected_id):
    writing_count = request.POST['this_product_count']
    for_key = LaboratoryOrder.objects.filter(id=1)[0]
    pr_id = LaboratoryItem.objects.filter(id=selected_id)[0]
    item = LaboratoryOrderItems(order=for_key, product_id=pr_id, amount=writing_count)
    item.save()
    return render(request, 'laboratory_item_information.html', {
        'data': LaboratoryItem.objects.filter(id=selected_id),
        'cart': LaboratoryOrderItems.objects.filter(order=1).count()})

def DelLaboratoryItem(request, selected_id):
    LaboratoryOrderItems.objects.filter(order=selected_id).delete()
    final_price = 0
    return render(request, 'laboratory_cart.html', {
        'data': LaboratoryItem.objects.filter(laboratoryorderitems__order=1),
        'final_price': final_price
    })