# Markaz

**Kuwait Cybersecurity Research Centre**
A control centre for open cybersecurity research, tooling and resources from Kuwait.

[Open the catalogue](https://siteq8.github.io/Markaz/) · [العربية](#مركز)

---

## What this is

Markaz publishes open regulatory data for Kuwait and the Gulf, and indexes the tooling
built against it.

The data comes first. Kuwait's cybersecurity instruments exist as PDFs and as logic
buried inside applications, which means practitioners cannot query them, researchers
cannot cite them, and nobody can check them. The centre publishes them as versioned
datasets with the provenance made explicit.

| Dataset | Instrument | Records |
| --- | --- | --- |
| [`kw-nbcc`](corpus/kw-nbcc/) | NCSC Decision No. 2 of 2026, national baseline | 44 controls |
| [`kw-corf`](corpus/kw-corf/) | CBK Cyber and Operational Resilience Framework v1.0 | 874 controls |

Every `kw-nbcc` record separates text quoted from the Annex from analysis added here,
and the build fails if the two are ever confused. See [the corpus](corpus/) for the
rule and its known limitations.

Three further things make it a centre rather than a profile page:

**It separates original research from mirrored work.** 107 original projects are
catalogued. 32 forks and mirrors of other people's work are listed apart, clearly
labelled, so credit is never blurred.

**It is fully bilingual with no mixing.** English mode is entirely English, Arabic mode
is entirely Arabic. Every project carries a hand written description in both languages,
and the build fails if a single Latin word leaks into an Arabic description or a single
Arabic character into an English one.

**It rebuilds from source.** The catalogue is generated from the GitHub API, not
maintained by hand, so it cannot drift. A new repository that is not classified in the
taxonomy fails the build rather than silently disappearing.

## Domains

| Domain | Projects |
| --- | --- |
| Kuwait and GCC Frameworks | 17 |
| Offensive Security | 10 |
| Forensics and Threat Hunting | 9 |
| Community and Civic | 9 |
| Global Compliance | 8 |
| Exposure and Brand Protection | 8 |
| ICS, OT and IoT | 7 |
| Asset and Network Discovery | 7 |
| Education and Awareness | 7 |
| Cloud and Infrastructure | 5 |
| Security Architecture | 5 |
| Governance and Leadership | 5 |
| AI and Agent Security | 4 |
| Cryptography and PQC | 3 |
| System Hardening | 3 |

## Rebuilding the catalogue

```
GITHUB_TOKEN=your_token python3 scripts/build_catalog.py
python3 scripts/build_site.py
```

The first command pulls live metadata and refuses to finish if any repository is
missing from `scripts/taxonomy.py`. The second embeds the data into `index.html` and
refuses to finish if either language is impure. The published page carries no external
request of any kind and works from the local filesystem.

## Publications

Research notes live in `publications/`, numbered and dated. See the
[publication guide](publications/README.md) for the format and the citation process.

## Licence

MIT. Individual projects in the catalogue carry their own licences, shown on
each card.

---

# مركز

**مركز الكويت لأبحاث الأمن السيبراني**
مركز تحكّم لأبحاث الأمن السيبراني المفتوحة وأدواتها ومواردها من الكويت.

[افتح الكتالوج](https://siteq8.github.io/Markaz/)

## ما هذا المركز

ينشر مركز بيانات تنظيمية مفتوحة للكويت والخليج، ثم يفهرس الأدوات المبنية عليها.

والبيانات تأتي أولاً، لأن الأدوات التشريعية الكويتية موجودة في ملفات مطبوعة أو محبوسة
داخل منطق التطبيقات، ما يعني أن الممارس لا يستطيع الاستعلام عنها ولا الباحث اقتباسها
ولا أحد التحقق منها، لذا ينشرها المركز مدوناتٍ مؤرشفةً بإصدارات ويصرّح فيها بمصدر كل
حقل.

| المدونة | الأداة التشريعية | السجلات |
| --- | --- | --- |
| `kw-nbcc` | قرار المركز الوطني رقم ٢ لسنة ٢٠٢٦ | ٤٤ ضابطاً |
| `kw-corf` | إطار المرونة السيبرانية والتشغيلية لبنك الكويت المركزي | ٨٧٤ ضابطاً |

يفصل كل سجل في المدونة الأولى بين النص المنقول من الملحق والتحليل المضاف هنا، ثم يسقط
البناء إذا اختلط الاثنان.

وثلاثة أمور أخرى تجعله مركزاً لا صفحة تعريف:

**يفصل العمل الأصيل عن المنسوخ،** فقد فُهرس مئة وسبعة مشاريع أصيلة بينما وُضعت اثنان
وثلاثون نسخةً من أعمال آخرين في قسم منفصل موسوم بوضوح كي لا يختلط النسب على أحد.

**ثنائي اللغة بلا خلط،** فالوضع الإنجليزي إنجليزي بالكامل والوضع العربي عربي بالكامل،
ولكل مشروع وصف مكتوب بخط اليد في اللغتين، ثم يفشل البناء إذا تسربت كلمة لاتينية واحدة
إلى وصف عربي أو حرف عربي واحد إلى وصف إنجليزي.

**يُبنى من المصدر،** إذ يُولَّد الكتالوج من واجهة غِت هَب البرمجية لا يدوياً لذا لا
يمكن أن ينحرف عن الواقع، وأي مستودع جديد غير مصنَّف في الشجرة يُسقِط البناء بدل أن
يختفي بصمت.

## إعادة بناء الكتالوج

```
GITHUB_TOKEN=your_token python3 scripts/build_catalog.py
python3 scripts/build_site.py
```

يسحب الأمر الأول البيانات الحيّة ويرفض الإتمام إن غاب أي مستودع عن الشجرة، ثم يدمج
الأمر الثاني البيانات في الصفحة ويرفض الإتمام إن اختلّت نقاء اللغة، والصفحة المنشورة
لا تُصدر أي طلب خارجي وتعمل من نظام الملفات المحلي.

## الأبحاث

تُحفظ الأوراق البحثية في مجلد `publications` مرقَّمةً ومؤرَّخةً، وفي دليل النشر تفصيل
الصيغة وآلية الاقتباس.

## الرخصة

رخصة إم آي تي، أما المشاريع المفهرسة فلكل منها رخصته الخاصة المعروضة على بطاقته.
