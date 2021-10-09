# -*- coding: UTF-8 -*-
from unishox2 import *
import unittest

class TestUnishox2(unittest.TestCase):

  usx2 = Unishox2()
  buf = bytearray(512)
  buf1 = bytearray(512)

  def run_test(self, str):
    utf8arr = bytearray(str, "utf-8")
    buf_len = self.usx2.unishox2_compress(str, len(str), self.buf, self.usx2.USX_HCODES_DFLT, self.usx2.USX_HCODE_LENS_DFLT, self.usx2.USX_FREQ_SEQ_DFLT, self.usx2.USX_TEMPLATES)
    out_str = self.usx2.unishox2_decompress(self.buf, buf_len, None, self.usx2.USX_HCODES_DFLT, self.usx2.USX_HCODE_LENS_DFLT, self.usx2.USX_FREQ_SEQ_DFLT, self.usx2.USX_TEMPLATES)
    buf_len = self.usx2.unishox2_compress(utf8arr, len(utf8arr), self.buf, self.usx2.USX_HCODES_DFLT, self.usx2.USX_HCODE_LENS_DFLT, self.usx2.USX_FREQ_SEQ_DFLT, self.usx2.USX_TEMPLATES)
    out_len = self.usx2.unishox2_decompress(self.buf, buf_len, self.buf1, self.usx2.USX_HCODES_DFLT, self.usx2.USX_HCODE_LENS_DFLT, self.usx2.USX_FREQ_SEQ_DFLT, self.usx2.USX_TEMPLATES)
    out_str1 = self.buf1[0 : out_len].decode("utf-8")
    input_len = len(utf8arr) #encodeURI(str).split(/%..|./).length - 1;
    self.assertEqual(out_str, str)
    self.assertEqual(out_str1, str)

    #input_arr[input_arr.length] = str;
    #out_len = usx2.unishox2_compress(input_arr, input_arr.length - 1, buf1, USX_HCODES_DFLT, USX_HCODE_LENS_DFLT, USX_FREQ_SEQ_DFLT, USX_TEMPLATES);
    ##compressed_arr[compressed_arr.length] = buf1.slice(0, out_len);
    #tot_input_len += utf8arr.length;
    #tot_comp_len += out_len;

  def test_Hello(self):
    self.run_test("Hello")

  def test_Hello_World(self):
    self.run_test("Hello World")

  def test_abc26(self):
    self.run_test("The quick brown fox jumped over the lazy dog")

  def test_HELLO_WORLD(self):
    self.run_test("HELLO WORLD")

  def test_HELLO_WORLD2(self):
    self.run_test("HELLO WORLD HELLO WORLD")

  def test_Hello1(self):
    self.run_test("Hello1")

  def test_Hello1_World2(self):
    self.run_test("Hello1 World2")

  def test_Hello123(self):
    self.run_test("Hello123")

  def test_12345678(self):
    self.run_test("12345678")

  def test_num4(self):
    self.run_test("12345678 12345678")

  def test_num5(self):
    self.run_test("HELLO WORLD 1234 hello world12")

  def test_num6(self):
    self.run_test("HELLO 234 WORLD")

  def test_num7(self):
    self.run_test("9 HELLO, WORLD")

  def test_num8(self):
    self.run_test("H1e2l3l4o5 w6O7R8L9D")

  def test_num9(self):
    self.run_test("8+80=88")

  def test_sym1(self):
    self.run_test("~!@#$%^&*()_+=-`;'\\|\":,./?><")

  def test_sym2(self):
    self.run_test("\"H1e2l3l4o5 w6O7R8L9D\"")

  def test_sym3(self):
    self.run_test("Hello\tWorld\tHow\tare\tyou?")

  def test_sym4(self):
    self.run_test("Hello~World~How~are~you?")

  def test_sym5(self):
    self.run_test("Hello\rWorld\rHow\rare\ryou?")

  def test_rpt1(self):
    self.run_test("-----------------///////////////")

  def test_rpt2(self):
    self.run_test("-----------------Hello World1111111111112222222abcdef12345abcde1234_////////Hello World///////")

  def test_nib1(self):
    self.run_test("fa01b51e-7ecc-4e3e-be7b-918a4c2c891c")

  def test_nib2(self):
    self.run_test("Fa01b51e-7ecc-4e3e-be7b-918a4c2c891c")

  def test_nib3(self):
    self.run_test("fa01b51e-7ecc-4e3e-be7b-9182c891c")

  def test_nib4(self):
    self.run_test("760FBCA3-272E-4F1A-BF88-8472DF6BD994")

  def test_nib5(self):
    self.run_test("760FBCA3-272E-4F1A-BF88-8472DF6Bd994")

  def test_nib6(self):
    self.run_test("760FBCA3-272E-4F1A-BF88-8472DF6Bg994")

  def test_nib7(self):
    self.run_test("FBCA3-272E-4F1A-BF88-8472DF6BD994")

  def test_nib8(self):
    self.run_test("Hello 1 5347a688-d8bf-445d-86d1-b470f95b007fHello World")

  def test_nib9(self):
    self.run_test("01234567890123")

  def test_tmpl1(self):
    self.run_test("2020-12-31")

  def test_tmpl2(self):
    self.run_test("1934-02")

  def test_tmpl3(self):
    self.run_test("2020-12-31T12:23:59.234Z")

  def test_tmpl4(self):
    self.run_test("1899-05-12T23:59:59.23434")

  def test_tmpl5(self):
    self.run_test("1899-05-12T23:59:59")

  def test_tmpl6(self):
    self.run_test("2020-12-31T12:23:59.234Zfa01b51e-7ecc-4e3e-be7b-918a4c2c891c")

  def test_tmpl7(self):
    self.run_test("顔に(993) 345-3495あり")

  def test_tmpl8(self):
    self.run_test("HELLO(993) 345-3495WORLD")

  def test_tmpl9(self):
    self.run_test("顔に1899-05-12T23:59:59あり")

  def test_tmpl10(self):
    self.run_test("HELLO1899-05-12T23:59:59WORLD")

  def test_spanish1(self):
    self.run_test("Cada buhonero alaba sus agujas. - A peddler praises his needles (wares).")

  def test_spanish2(self):
    self.run_test("Cada gallo canta en su muladar. - Each rooster sings on its dung-heap.")

  def test_spanish3(self):
    self.run_test("Cada martes tiene su domingo. - Each Tuesday has its Sunday.")

  def test_spanish4(self):
    self.run_test("Cada uno habla de la feria como le va en ella. - Our way of talking about things reflects our relevant experience, good or bad.")

  def test_spanish5(self):
    self.run_test("Dime con quien andas y te diré quién eres.. - Tell me who you walk with, and I will tell you who you are.")

  def test_spanish6(self):
    self.run_test("Donde comen dos, comen tres. - You can add one person more in any situation you are managing.")

  def test_spanish7(self):
    self.run_test("El amor es ciego. - Love is blind")

  def test_spanish8(self):
    self.run_test("El amor todo lo iguala. - Love smoothes life out.")

  def test_spanish9(self):
    self.run_test("El tiempo todo lo cura. - Time cures all.")

  def test_spanish10(self):
    self.run_test("La avaricia rompe el saco. - Greed bursts the sack.")

  def test_spanish11(self):
    self.run_test("La cara es el espejo del alma. - The face is the mirror of the soul.")

  def test_spanish12(self):
    self.run_test("La diligencia es la madre de la buena ventura. - Diligence is the mother of good fortune.")

  def test_spanish13(self):
    self.run_test("La fe mueve montañas. - Faith moves mountains.")

  def test_spanish14(self):
    self.run_test("La mejor palabra siempre es la que queda por decir. - The best word is the one left unsaid.")

  def test_spanish15(self):
    self.run_test("La peor gallina es la que más cacarea. - The worst hen is the one that clucks the most.")

  def test_spanish16(self):
    self.run_test("La sangre sin fuego hierve. - Blood boils without fire.")

  def test_spanish17(self):
    self.run_test("La vida no es un camino de rosas. - Life is not a path of roses.")

  def test_spanish18(self):
    self.run_test("Las burlas se vuelven veras. - Bad jokes become reality.")

  def test_spanish19(self):
    self.run_test("Las desgracias nunca vienen solas. - Misfortunes never come one at a time.")

  def test_spanish20(self):
    self.run_test("Lo comido es lo seguro. - You can only be really certain of what is already in your belly.")

  def test_spanish21(self):
    self.run_test("Los años no pasan en balde. - Years don't pass in vain.")

  def test_spanish22(self):
    self.run_test("Los celos son malos consejeros. - Jealousy is a bad counsellor.")

  def test_spanish23(self):
    self.run_test("Los tiempos cambian. - Times change.")

  def test_spanish24(self):
    self.run_test("Mañana será otro día. - Tomorrow will be another day.")

  def test_spanish25(self):
    self.run_test("Ningún jorobado ve su joroba. - No hunchback sees his own hump.")

  def test_spanish26(self):
    self.run_test("No cantan dos gallos en un gallinero. - Two roosters do not crow in a henhouse.")

  def test_spanish27(self):
    self.run_test("No hay harina sin salvado. - No flour without bran.")

  def test_spanish28(self):
    self.run_test("No por mucho madrugar, amanece más temprano.. - No matter if you rise early because it does not sunrise earlier.")

  def test_spanish29(self):
    self.run_test("No se puede hacer tortilla sin romper los huevos. - One can't make an omelette without breaking eggs.")

  def test_spanish30(self):
    self.run_test("No todas las verdades son para dichas. - Not every truth should be said.")

  def test_spanish31(self):
    self.run_test("No todo el monte es orégano. - The whole hillside is not covered in spice.")

  def test_spanish32(self):
    self.run_test("Nunca llueve a gusto de todos. - It never rains to everyone's taste.")

  def test_spanish33(self):
    self.run_test("Perro ladrador, poco mordedor.. - A dog that barks often seldom bites.")

  def test_spanish34(self):
    self.run_test("Todos los caminos llevan a Roma. - All roads lead to Rome.")

  def test_japanese1(self):
    self.run_test("案ずるより産むが易し。 - Giving birth to a baby is easier than worrying about it.")

  def test_japanese2(self):
    self.run_test("出る杭は打たれる。 - The stake that sticks up gets hammered down.")

  def test_japanese3(self):
    self.run_test("知らぬが仏。 - Not knowing is Buddha. - Ignorance is bliss.")

  def test_japanese4(self):
    self.run_test("見ぬが花。 - Not seeing is a flower. - Reality can't compete with imagination.")

  def test_japanese5(self):
    self.run_test("花は桜木人は武士 - Of flowers, the cherry blossom; of men, the warrior.")

  def test_chinese1(self):
    self.run_test("小洞不补，大洞吃苦 - A small hole not mended in time will become a big hole much more difficult to mend.")

  def test_chinese2(self):
    self.run_test("读万卷书不如行万里路 - Reading thousands of books is not as good as traveling thousands of miles")

  def test_chinese3(self):
    self.run_test("福无重至,祸不单行 - Fortune does not come twice. Misfortune does not come alone.")

  def test_chinese4(self):
    self.run_test("风向转变时,有人筑墙,有人造风车 - When the wind changes, some people build walls and have artificial windmills.")

  def test_chinese5(self):
    self.run_test("父债子还 - Father's debt, son to give back.")

  def test_chinese6(self):
    self.run_test("害人之心不可有 - Do not harbour intentions to hurt others.")

  def test_chinese7(self):
    self.run_test("今日事，今日毕 - Things of today, accomplished today.")

  def test_chinese8(self):
    self.run_test("空穴来风,未必无因 - Where there's smoke, there's fire.")

  def test_chinese9(self):
    self.run_test("良药苦口 - Good medicine tastes bitter.")

  def test_chinese10(self):
    self.run_test("人算不如天算 - Man proposes and God disposes")

  def test_chinese11(self):
    self.run_test("师傅领进门，修行在个人 - Teachers open the door. You enter by yourself.")

  def test_chinese12(self):
    self.run_test("授人以鱼不如授之以渔 - Teach a man to take a fish is not equal to teach a man how to fish.")

  def test_chinese13(self):
    self.run_test("树倒猢狲散 - When the tree falls, the monkeys scatter.")

  def test_chinese14(self):
    self.run_test("水能载舟，亦能覆舟 - Not only can water float a boat, it can sink it also.")

  def test_chinese15(self):
    self.run_test("朝被蛇咬，十年怕井绳 - Once bitten by a snake for a snap dreads a rope for a decade.")

  def test_chinese16(self):
    self.run_test("一分耕耘，一分收获 - If one does not plow, there will be no harvest.")

  def test_chinese17(self):
    self.run_test("有钱能使鬼推磨 - If you have money you can make the devil push your grind stone.")

  def test_chinese18(self):
    self.run_test("一失足成千古恨，再回头\n已百年身 - A single slip may cause lasting sorrow.")

  def test_chinese19(self):
    self.run_test("自助者天助 - Those who help themselves, God will help.")

  def test_chinese20(self):
    self.run_test("早起的鸟儿有虫吃 - Early bird gets the worm.")

  def test_chinese21(self):
    self.run_test("This is first line,\r\nThis is second line")

  def test_chinese22(self):
    self.run_test("{\"menu\": {\n  \"id\": \"file\",\n  \"value\": \"File\",\n  \"popup\": {\n    \"menuitem\": [\n      {\"value\": \"New\", \"onclick\": \"CreateNewDoc()\"},\n      {\"value\": \"Open\", \"onclick\": \"OpenDoc()\"},\n      {\"value\": \"Close\", \"onclick\": \"CloseDoc()\"}\n    ]\n  }\n}}")

  def test_chinese23(self):
    self.run_test("{\"menu\": {\r\n  \"id\": \"file\",\r\n  \"value\": \"File\",\r\n  \"popup\": {\r\n    \"menuitem\": [\r\n      {\"value\": \"New\", \"onclick\": \"CreateNewDoc()\"},\r\n      {\"value\": \"Open\", \"onclick\": \"OpenDoc()\"},\r\n      {\"value\":\"Close\", \"onclick\": \"CloseDoc()\"}\r\n    ]\r\n  }\r\n}}")

  def test_chinese24(self):
    self.run_test("https://siara.cc")

  def test_chinese25(self):
    self.run_test("符号\"δ\"表")

  def test_chinese26(self):
    self.run_test("学者地”[3]。学者")

  def test_chinese27(self):
    self.run_test("한데......아무")

  def test_Beauty_English(self):
    self.run_test("Beauty is not in the face. Beauty is a light in the heart.")

  def test_Beauty_Spanish(self):
    self.run_test("La belleza no está en la cara. La belleza es una luz en el corazón.")

  def test_Beauty_French(self):
    self.run_test("La beauté est pas dans le visage. La beauté est la lumière dans le coeur.")

  def test_Beauty_Portugese(self):
    self.run_test("A beleza não está na cara. A beleza é a luz no coração.")

  def test_Beauty_Dutch(self):
    self.run_test("Schoonheid is niet in het gezicht. Schoonheid is een licht in het hart.")

  def test_Beauty_German(self):
    self.run_test("Schönheit ist nicht im Gesicht. Schönheit ist ein Licht im Herzen.")

  def test_Beauty_Spanish(self):
    self.run_test("La belleza no está en la cara. La belleza es una luz en el corazón.")

  def test_Beauty_French(self):
    self.run_test("La beauté est pas dans le visage. La beauté est la lumière dans le coeur.")

  def test_Beauty_Italian(self):
    self.run_test("La bellezza non è in faccia. La bellezza è la luce nel cuore.")

  def test_Beauty_Swedish(self):
    self.run_test("Skönhet är inte i ansiktet. Skönhet är ett ljus i hjärtat.")

  def test_Beauty_Romanian(self):
    self.run_test("Frumusețea nu este în față. Frumusețea este o lumină în inimă.")

  def test_Beauty_Ukranian(self):
    self.run_test("Краса не в особі. Краса - це світло в серці.")

  def test_Beauty_Greek(self):
    self.run_test("Η ομορφιά δεν είναι στο πρόσωπο. Η ομορφιά είναι ένα φως στην καρδιά.")

  def test_Beauty_Turkish(self):
    self.run_test("Güzellik yüzünde değil. Güzellik, kalbin içindeki bir ışıktır.")

  def test_Beauty_Polish(self):
    self.run_test("Piękno nie jest na twarzy. Piękno jest światłem w sercu.")

  def test_Beauty_Africans(self):
    self.run_test("Skoonheid is nie in die gesig nie. Skoonheid is 'n lig in die hart.")

  def test_Beauty_Swahili(self):
    self.run_test("Beauty si katika uso. Uzuri ni nuru moyoni.")

  def test_Beauty_Zulu(self):
    self.run_test("Ubuhle abukho ebusweni. Ubuhle bungukukhanya enhliziyweni.")

  def test_Beauty_Somali(self):
    self.run_test("Beauty ma aha in wajiga. Beauty waa iftiin ah ee wadnaha.")

  def test_Beauty_Russian(self):
    self.run_test("Красота не в лицо. Красота - это свет в сердце.")

  def test_Beauty_Arabic(self):
    self.run_test("الجمال ليس في الوجه. الجمال هو النور الذي في القلب.")

  def test_Beauty_Persian(self):
    self.run_test("زیبایی در چهره نیست. زیبایی نور در قلب است.")

  def test_Beauty_Pashto(self):
    self.run_test("ښکلا په مخ کې نه ده. ښکلا په زړه کی یوه رڼا ده.")

  def test_Beauty_Azerbaijani(self):
    self.run_test("Gözəllik üzdə deyil. Gözəllik qəlbdə bir işıqdır.")

  def test_Beauty_Uzbek(self):
    self.run_test("Go'zallik yuzida emas. Go'zallik - qalbdagi nur.")

  def test_Beauty_Kurdish(self):
    self.run_test("Bedewî ne di rû de ye. Bedewî di dil de ronahiyek e.")

  def test_Beauty_Urdu(self):
    self.run_test("خوبصورتی چہرے میں نہیں ہے۔ خوبصورتی دل میں روشنی ہے۔")

  def test_Beauty_Hindi(self):
    self.run_test("सुंदरता चेहरे में नहीं है। सौंदर्य हृदय में प्रकाश है।")

  def test_Beauty_Bangla(self):
    self.run_test("সৌন্দর্য মুখে নেই। সৌন্দর্য হৃদয় একটি আলো।")

  def test_Beauty_Punjabi(self):
    self.run_test("ਸੁੰਦਰਤਾ ਚਿਹਰੇ ਵਿੱਚ ਨਹੀਂ ਹੈ. ਸੁੰਦਰਤਾ ਦੇ ਦਿਲ ਵਿਚ ਚਾਨਣ ਹੈ.")

  def test_Beauty_Telugu(self):
    self.run_test("అందం ముఖంలో లేదు. అందం హృదయంలో ఒక కాంతి.")

  def test_Beauty_Tamil(self):
    self.run_test("அழகு முகத்தில் இல்லை. அழகு என்பது இதயத்தின் ஒளி.")

  def test_Beauty_Marathi(self):
    self.run_test("सौंदर्य चेहरा नाही. सौंदर्य हे हृदयातील एक प्रकाश आहे.")

  def test_Beauty_Kannada(self):
    self.run_test("ಸೌಂದರ್ಯವು ಮುಖದ ಮೇಲೆ ಇಲ್ಲ. ಸೌಂದರ್ಯವು ಹೃದಯದಲ್ಲಿ ಒಂದು ಬೆಳಕು.")

  def test_Beauty_Gujarati(self):
    self.run_test("સુંદરતા ચહેરા પર નથી. સુંદરતા હૃદયમાં પ્રકાશ છે.")

  def test_Beauty_Malayalam(self):
    self.run_test("സൗന്ദര്യം മുഖത്ത് ഇല്ല. സൗന്ദര്യം ഹൃദയത്തിലെ ഒരു പ്രകാശമാണ്.")

  def test_Beauty_Nepali(self):
    self.run_test("सौन्दर्य अनुहारमा छैन। सौन्दर्य मुटुको उज्यालो हो।")

  def test_Beauty_Sinhala(self):
    self.run_test("රූපලාවන්ය මුහුණේ නොවේ. රූපලාවන්ය හදවත තුළ ඇති ආලෝකය වේ.")

  def test_Beauty_Chinese(self):
    self.run_test("美是不是在脸上。 美是心中的亮光。")

  def test_Beauty_Javanese(self):
    self.run_test("Beauty ora ing pasuryan. Kaendahan iku cahya ing sajroning ati.")

  def test_Beauty_chinese(self):
    self.run_test("美は顔にありません。美は心の中の光です。")

  def test_Beauty_Filipino(self):
    self.run_test("Ang kagandahan ay wala sa mukha. Ang kagandahan ay ang ilaw sa puso.")

  def test_Beauty_Korean(self):
    self.run_test("아름다움은 얼굴에 없습니다。아름다움은 마음의 빛입니다。")

  def test_Beauty_Vietnam(self):
    self.run_test("Vẻ đẹp không nằm trong khuôn mặt. Vẻ đẹp là ánh sáng trong tim.")

  def test_Beauty_Thai(self):
    self.run_test("ความงามไม่ได้อยู่ที่ใบหน้า ความงามเป็นแสงสว่างในใจ")

  def test_Beauty_Burmese(self):
    self.run_test("အလှအပမျက်နှာပေါ်မှာမဟုတ်ပါဘူး။ အလှအပစိတ်နှလုံးထဲမှာအလင်းကိုဖြစ်ပါတယ်။")

  def test_Beauty_Malay(self):
    self.run_test("Kecantikan bukan di muka. Kecantikan adalah cahaya di dalam hati.")

  def test_Emoji1(self):
    self.run_test("🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣")

  def test_Emoji2(self):
    self.run_test("😀😃😄😁😆😅🤣😂🙂🙃😉😊😇🥰😍🤩😘😗😚😙😋😛😜🤪😝🤑🤗🤭🤫🤔🤐🤨😐😑😶😏😒🙄😬🤥😌😔😪🤤😴😷🤒🤕🤢")

if __name__ == '__main__':
    unittest.main()
