# تصميم BrowserTrace

## بيانات المشروع

المالك: Ali Abdullah Mohammed Rajeh. الرقم الجامعي: 25164073. المجموعة: G2.

## المعمارية العامة

```text
CLI / Shell
    |
Scanner -> Registry -> Browser Family Handler
    |                 |
    +-> Extractor ----+-> SQLite / JSON / plist
    |
Analyzer -> Filters -> Table Renderer
    |
Reporters -> JSON / CSV / HTML
```

## الوحدات

- `cli.py`: تحليل أوامر التشغيل.
- `shell.py`: الغلاف التفاعلي.
- `core/scanner.py`: اكتشاف المسارات والملفات الشخصية.
- `core/extractor.py`: استخراج البيانات.
- `core/analyzer.py`: المرشحات والتحويلات.
- `core/credential_export.py`: تصدير الكتل المشفرة.
- `browsers/`: الواجهات العائلية وسجل المتصفحات.
- `reporters/`: JSON وCSV وHTML.
- `ui/`: الألوان والجداول والتقدم والرسائل.

## تدفق البيانات

```text
Browser Registry
      |
Profile Discovery
      |
Copy DB to Temporary File
      |
Read-Only SQLite Query
      |
Normalize Records
      |
Filter
      |
Limit
      |
Render or Export
```

## CLI

عند عدم وجود معاملات تظهر واجهة تفاعلية. عند وجود معاملات ينفذ الأمر مرة واحدة.

## الألوان والشعار

يتم تعريف ANSI في `assets/colors.py` فقط. الألوان تتوقف إذا لم يكن stdout طرفية أو عند `NO_COLOR` أو `--no-color`.

## الجداول

محرك الجدول يحسب عرض الأعمدة، يختصر القيم الطويلة، ويحافظ على حد أقصى لعرض الطرفية.

## registry.py

السجل هو مصدر الحقيقة الوحيد ويحتوي بالضبط على عشرين مفتاحًا. إضافة متصفح جديد تتطلب إضافة سجل فقط ما لم يحتج سلوكًا خاصًا.

## لماذا لا يوجد ملف لكل متصفح

التكرار يرفع تكلفة الصيانة ويزيد أخطاء المسارات والاستعلامات. العائلات تسمح بإعادة استخدام المنطق مع اختلافات البيانات في Registry.

## الحزمة التنفيذية

تستخدم `zipapp` لإنشاء `browsertrace.pyz`. هذا ليس ملف EXE أصليًا، ولكنه ملف Python واحد قابل للنقل ويعمل دون مكتبات خارجية.
