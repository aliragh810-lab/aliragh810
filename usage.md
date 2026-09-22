# دليل استخدام BrowserTrace

## بيانات المشروع

BrowserTrace 1.0.0، المالك Ali Abdullah Mohammed Rajeh، الرقم الجامعي 25164073، المجموعة G2.

## التثبيت

شغّل:

`python browsertrace.pyz install`

ثم تحقق:

`browsertrace --version`

## البدء السريع

`python -m browsertrace scan`

`python -m browsertrace history --browser chrome --limit 20`

`python -m browsertrace downloads --browser chrome --limit 10`

## الأوامر

- `scan`: اكتشاف المتصفحات والملفات الشخصية.
- `history`: استخراج سجل التصفح.
- `downloads`: استخراج التنزيلات.
- `cookies`: استخراج بيانات الكوكيز الوصفية فقط.
- `bookmarks`: استخراج الإشارات المرجعية.
- `autofill`: استخراج الملء التلقائي.
- `logins`: استخراج بيانات تسجيل الدخول الوصفية فقط.
- `passwords` أو `creds`: تصدير الكتل المشفرة بعد التأكيد.
- `search`: استخراج عبارات البحث.
- `extensions`: عرض الإضافات.
- `report`: تقرير شامل.
- `list-browsers`: عرض المتصفحات المدعومة.
- `config`: عرض أو تعديل الإعدادات الأساسية.
- `install`: تثبيت الحزمة.
- `uninstall`: إزالة التثبيت.
- `about`: معلومات الأداة.
- `version`: الإصدار.

## --limit

`--limit 10` يعرض أول عشر نتائج. `--limit 0` يعرض الكل ويحذر عند تجاوز 1000.

## المرشحات

يمكن استخدام `--since`, `--until`, `--domain`, `--keyword`, `--file-type`.

## كلمات المرور المشفرة

قبل `passwords` ستظهر رسالة قانونية وتطلب تأكيدًا. لا يتم فك التشفير ولا تعرض القيم المشفرة على الشاشة.

## الأخطاء الشائعة

إذا كان المتصفح يعمل فقد تكون قاعدة البيانات مقفلة؛ الأداة تنسخها إلى ملف مؤقت أولًا. إذا لم توجد قاعدة أو ملف شخصي، يظهر تنبيه نظيف بدل traceback.
