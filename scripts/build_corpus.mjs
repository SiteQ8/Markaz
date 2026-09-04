/*
 * Extracts the Kuwait NBCC corpus from the Kuwait-NBCC package into a plain,
 * versioned dataset that does not require the package to read.
 *
 * The point of the extraction is provenance. Each control carries official text
 * quoted from the Annex alongside editorial material written by the project,
 * and the two must never be confused by a downstream consumer. Every field that
 * originates with this project rather than with the Decision is marked, and the
 * extractor fails rather than emitting a record whose provenance is unclear.
 *
 * Usage:
 *   node scripts/build_corpus.mjs /path/to/Kuwait-NBCC
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const source = process.argv[2];
if (!source) {
  console.error('Usage: node scripts/build_corpus.mjs /path/to/Kuwait-NBCC');
  process.exit(2);
}

const src = (p) => pathToFileURL(resolve(source, p)).href;
const { CONTROLS, REGULATION, FUNCTIONS } = await import(src('src/catalog.js'));
const { FRAMEWORKS, ISO_MAP } = await import(src('src/crosswalk.js'));
const pkg = JSON.parse(readFileSync(resolve(source, 'package.json'), 'utf8'));

const OUT = resolve(process.cwd(), 'corpus/kw-nbcc');
mkdirSync(OUT, { recursive: true });

const faults = [];

/* Official text is what the Annex prints. Everything else is this project's
 * own work and is labelled so that a reader can tell them apart without
 * consulting the gazette. */
const controls = CONTROLS.map((c) => {
  if (!c.id || !c.requirement) faults.push(`${c.id || '(no id)'}: missing requirement`);
  if (c.purpose && !c.purposeSource) faults.push(`${c.id}: purpose without a purposeSource`);
  if (!c.titleAr || !c.requirementAr) faults.push(`${c.id}: incomplete Arabic`);

  const editorialPurpose = c.purposeSource !== 'annex';

  return {
    id: c.id,
    function: c.fn,
    official: {
      title: c.title,
      titleAr: c.titleAr,
      requirement: c.requirement,
      requirementAr: c.requirementAr,
      purpose: editorialPurpose ? null : c.purpose,
      purposeAr: editorialPurpose ? null : c.purposeAr
    },
    editorial: {
      purpose: editorialPurpose ? c.purpose ?? null : null,
      purposeAr: editorialPurpose ? c.purposeAr ?? null : null,
      checks: c.checks ?? [],
      checksAr: c.checksAr ?? [],
      evidence: c.evidence ?? [],
      evidenceAr: c.evidenceAr ?? [],
      cadence: c.cadence ?? null,
      effort: c.effort ?? null,
      phase: c.phase ?? null,
      beyondAnnex: c.beyondAnnex ?? []
    },
    appliesWhen: c.appliesWhen ?? [],
    crosswalk: {
      csf: c.crosswalk?.csf ?? [],
      cis: c.crosswalk?.cis ?? [],
      iso: ISO_MAP?.[c.id] ?? []
    }
  };
});

if (faults.length) {
  console.error('Extraction refused, provenance is unclear:');
  faults.forEach((f) => console.error(`  ${f}`));
  process.exit(1);
}

const byFunction = {};
for (const c of controls) byFunction[c.function] = (byFunction[c.function] || 0) + 1;

const dataset = {
  dataset: 'kw-nbcc',
  title: 'Kuwait National Basic Cybersecurity Controls, machine readable corpus',
  titleAr: 'الضوابط الوطنية الأساسية للأمن السيبراني، مدونة مقروءة آليا',
  sourceVersion: pkg.version,
  extracted: new Date().toISOString().slice(0, 10),
  licence: 'MIT',
  provenance: {
    note: 'Fields under official are quoted from the Annex. Fields under editorial are this project\'s own analysis and carry no official standing.',
    noteAr: 'الحقول تحت official منقولة من الملحق، أما الحقول تحت editorial فهي تحليل خاص بهذا المشروع ولا تحمل أي صفة رسمية.'
  },
  regulation: REGULATION,
  functions: FUNCTIONS,
  frameworks: FRAMEWORKS,
  counts: {
    controls: controls.length,
    byFunction,
    withCsf: controls.filter((c) => c.crosswalk.csf.length).length,
    withCis: controls.filter((c) => c.crosswalk.cis.length).length,
    withIso: controls.filter((c) => c.crosswalk.iso.length).length,
    officialPurpose: controls.filter((c) => c.official.purpose).length,
    editorialPurpose: controls.filter((c) => c.editorial.purpose).length
  },
  controls
};

writeFileSync(`${OUT}/controls.json`, JSON.stringify(dataset, null, 2) + '\n');

/* A flat table so the corpus is usable without a JSON parser. */
const esc = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
const rows = [
  ['id', 'function', 'title', 'title_ar', 'requirement', 'requirement_ar',
   'purpose_is_official', 'csf', 'cis', 'iso', 'phase', 'effort'].join(','),
  ...controls.map((c) => [
    c.id, c.function, c.official.title, c.official.titleAr,
    c.official.requirement, c.official.requirementAr,
    c.official.purpose ? 'yes' : 'no',
    c.crosswalk.csf.join(' '), c.crosswalk.cis.join(' '), c.crosswalk.iso.join(' '),
    c.editorial.phase, c.editorial.effort
  ].map(esc).join(','))
];
writeFileSync(`${OUT}/controls.csv`, rows.join('\n') + '\n');

console.log(`corpus/kw-nbcc/controls.json  ${dataset.counts.controls} controls`);
console.log(`corpus/kw-nbcc/controls.csv   flat table`);
console.log(`  by function      ${JSON.stringify(byFunction)}`);
console.log(`  official purpose ${dataset.counts.officialPurpose}`);
console.log(`  editorial purpose ${dataset.counts.editorialPurpose}`);
console.log(`  crosswalk csf/cis/iso  ${dataset.counts.withCsf}/${dataset.counts.withCis}/${dataset.counts.withIso}`);
