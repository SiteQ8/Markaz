# Markaz

**Kuwait Cybersecurity Research Centre**
A control centre for open cybersecurity research, tooling and resources from Kuwait.

[Open the catalogue](https://siteq8.github.io/Markaz/) · [العربية](#مركز)

---

## What this is

Markaz is the index over everything published under this account. It is not another
tool. It is the layer that makes 107 tools, control mappings and datasets findable,
citable and current.

Three things make it a research centre rather than a profile page:

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

مركز هو الفهرس الجامع لكل ما يُنشر تحت هذا الحساب، وهو ليس أداةً جديدةً تُضاف إلى
الأدوات بل الطبقة التي تجعل مئةً وسبعة مشاريع وربوط ضوابط ومجموعات بيانات قابلةً
للإيجاد والاقتباس والتحديث.

ثلاثة أمور تجعله مركز أبحاث لا صفحة تعريف:

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
