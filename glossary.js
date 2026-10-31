/* ============================================================
   CliniPD — hover glossary
   ------------------------------------------------------------
   Any term in GLOSSARY below is detected automatically in page
   prose and given a dotted underline. Hover (or tap on touch)
   shows a short definition.

   TO ADD A TERM: add one line to GLOSSARY. Nothing else.
     "term": { d: "The definition.", s: "Optional source note" }

   Rules the matcher follows, so it never makes a mess:
     · only the FIRST occurrence of a term on a page is marked
     · never inside headings, links, buttons, code or form fields
     · longest term wins, so "likelihood ratio" beats "ratio"
     · whole words only, case-insensitive, plurals handled
   ============================================================ */

const GLOSSARY = {
  /* ---- reasoning & assessment ---- */
  "irritability": { d: "How easily symptoms are provoked, how severe they get, and how long they take to settle. Drives how vigorously you can assess and treat." },
  "SIN factors": { d: "Severity, Irritability and Nature — the three judgements that set the limits of a physical examination." },
  "end-feel": { d: "The quality of resistance felt at the end of passive range. Normal end-feels are soft, firm or hard; an empty or springy end-feel suggests pathology." },
  "concordant sign": { d: "A test that reproduces the patient's own familiar pain, rather than just any pain. Far more useful than a positive test alone." },
  "closed-packed position": { d: "The joint position of maximal congruency and ligamentous tension, where accessory movement is least available." },
  "loose-packed position": { d: "The joint position of least congruency, where capsular laxity is greatest and accessory movement is most available. Used for mobilisation." },
  "neurodynamics": { d: "Assessment and treatment of the nervous system's capacity to tolerate movement and load — testing mechanosensitivity rather than conduction." },
  "arthrokinematics": { d: "The accessory motion occurring at joint surfaces — roll, spin and glide — as distinct from the visible movement of the limb." },
  "osteokinematics": { d: "The gross, observable movement of bones about a joint axis, described in planes: flexion, abduction, rotation." },
  "capsular pattern": { d: "A characteristic proportional loss of passive range that suggests the joint capsule itself is the restricting structure." },
  "differential diagnosis": { d: "The set of conditions that could plausibly explain a presentation, and the reasoning used to separate them." },
  "red flag": { d: "A feature suggesting serious pathology that needs medical review rather than physiotherapy — fracture, infection, malignancy, cauda equina." },
  "yellow flag": { d: "A psychosocial factor predicting delayed recovery — fear-avoidance, low self-efficacy, catastrophising, unhelpful beliefs about pain." },

  /* ---- pain ---- */
  "nociceptive pain": { d: "Pain arising from actual or threatened damage to non-neural tissue, driven by activation of nociceptors. Typically proportionate to load and eases with rest." },
  "neuropathic pain": { d: "Pain caused by a lesion or disease of the somatosensory nervous system. Often burning or shooting, in a neuroanatomically plausible distribution." },
  "nociplastic pain": { d: "Pain arising from altered nociception without clear tissue damage or somatosensory lesion. The third mechanistic descriptor recognised by the IASP." },
  "central sensitisation": { d: "Increased responsiveness of central nociceptive neurons to normal or subthreshold input. Clinically: widespread, disproportionate, slow-settling pain." },
  "allodynia": { d: "Pain from a stimulus that does not normally provoke pain — light touch, clothing, a breeze." },
  "hyperalgesia": { d: "An exaggerated pain response to a stimulus that is normally painful." },
  "kinesiophobia": { d: "Fear of movement or re-injury. Measured with the Tampa Scale and a consistent predictor of poorer outcome." },
  "catastrophising": { d: "An exaggerated negative orientation toward pain — rumination, magnification and helplessness. Strongly predicts persistent disability." },
  "graded exposure": { d: "Progressively confronting feared movements in a planned way, targeting the fear rather than the tissue." },

  /* ---- measurement & evidence ---- */
  "sensitivity": { d: "The proportion of people WITH the condition that a test correctly identifies. A highly sensitive test, when negative, helps rule the condition out." },
  "specificity": { d: "The proportion of people WITHOUT the condition that a test correctly clears. A highly specific test, when positive, helps rule the condition in." },
  "likelihood ratio": { d: "How much a test result shifts the probability of a condition. Above 10 or below 0.1 produces large, often decisive shifts." },
  "pre-test probability": { d: "Your estimate that the condition is present before testing — from prevalence, history and examination. Test results modify it; they don't replace it." },
  "post-test probability": { d: "The revised probability of a condition after a test result has been applied to the pre-test probability." },
  "MCID": { d: "Minimal Clinically Important Difference — the smallest change in a score that a patient would consider worthwhile." },
  "MDC": { d: "Minimal Detectable Change — the smallest change exceeding measurement error. A change below the MDC cannot be distinguished from noise." },
  "PROM": { d: "Patient-Reported Outcome Measure — a questionnaire completed by the patient about their own symptoms, function or quality of life." },
  "NPRS": { d: "Numeric Pain Rating Scale — pain rated 0 to 10. MCID is roughly 2 points in most musculoskeletal populations." },
  "VAS": { d: "Visual Analogue Scale — pain marked on a 100 mm line. Comparable to the NPRS but more sensitive to small change." },
  "AKPS": { d: "Anterior Knee Pain Scale (Kujala) — a 13-item, 100-point measure of patellofemoral symptoms and function." },
  "KOOS": { d: "Knee injury and Osteoarthritis Outcome Score — five subscales covering pain, symptoms, daily living, sport and quality of life." },
  "confidence interval": { d: "The range within which the true value plausibly lies. A wide interval means the estimate is imprecise, whatever the point estimate says." },
  "effect size": { d: "How large a difference is, independent of sample size. Roughly: 0.2 small, 0.5 moderate, 0.8 large." },
  "number needed to treat": { d: "How many people must receive an intervention for one additional person to benefit. Lower is better." },
  "systematic review": { d: "A review that searches, appraises and synthesises all eligible studies to a pre-specified protocol — not the same as a narrative review." },
  "randomised controlled trial": { d: "A trial allocating participants to groups by chance, which balances known and unknown confounders. The strongest single-study design for effectiveness." },

  /* ---- exercise & loading ---- */
  "eccentric": { d: "A muscle action where the muscle lengthens under load. Produces higher force and more delayed-onset soreness than concentric work." },
  "concentric": { d: "A muscle action where the muscle shortens under load." },
  "isometric": { d: "A muscle action producing force with no change in muscle length. Often used for analgesia and early loading in tendinopathy." },
  "plyometric": { d: "Training using a rapid stretch-shortening cycle — jumping, hopping, bounding — to develop reactive strength." },
  "1RM": { d: "One-repetition maximum — the heaviest load that can be lifted once with acceptable technique. Used to prescribe relative intensity." },
  "RPE": { d: "Rating of Perceived Exertion — how hard an effort felt, typically 0 to 10. Allows load to self-adjust on bad days." },
  "MVC": { d: "Maximal Voluntary Contraction — the greatest force a muscle can generate voluntarily. Used as a reference for prescribing intensity." },
  "load capacity": { d: "How much load a tissue can tolerate before symptoms. Rehabilitation raises capacity; management reduces demand until the two meet." },
  "proprioception": { d: "The sense of joint position and movement, from receptors in muscle, tendon, joint capsule and skin." },
  "progressive overload": { d: "Gradually increasing demand so tissue continues to adapt. Without it, strength gains plateau." },
  "time under tension": { d: "The total duration a muscle is loaded during a set. A common variable for tendon loading protocols." },

  /* ---- anatomy & signs ---- */
  "valgus": { d: "Angulation where the distal segment deviates away from the midline — knock-kneed at the knee." },
  "varus": { d: "Angulation where the distal segment deviates toward the midline — bow-legged at the knee." },
  "crepitus": { d: "Audible or palpable grating, clicking or crackling in a joint. Common, usually benign, and poorly correlated with pathology." },
  "effusion": { d: "Excess fluid within a joint capsule. Graded by sweep test; a large tense effusion after trauma suggests haemarthrosis." },
  "haemarthrosis": { d: "Blood within a joint, usually appearing within two hours of injury. Strongly suggests ACL rupture, fracture or patellar dislocation." },
  "retropatellar": { d: "Behind the patella — describing pain arising from the patellofemoral joint surface." },
  "peripatellar": { d: "Around the margins of the patella." },
  "trochlea": { d: "The grooved articular surface of the distal femur in which the patella tracks." },
  "theatre sign": { d: "Anterior knee pain after prolonged sitting with the knee flexed. Characteristic of patellofemoral pain." },
  "apprehension": { d: "A patient's protective reaction and fear during a test that threatens joint stability — a positive finding in itself." },
  "antalgic gait": { d: "A limp adopted to reduce time or load on a painful limb, shortening the stance phase on that side." },
  "Trendelenburg sign": { d: "Pelvic drop on the unsupported side during single-leg stance, indicating hip abductor weakness on the stance side." },
  "dermatome": { d: "The area of skin supplied by a single spinal nerve root. Used to localise radicular involvement." },
  "myotome": { d: "The group of muscles supplied by a single spinal nerve root. Tested by resisted contraction." },
  "radiculopathy": { d: "Dysfunction of a spinal nerve root producing pain, sensory change, weakness or reflex loss in that root's distribution." },
  "referred pain": { d: "Pain felt away from its source, without nerve root involvement. Typically vague, non-dermatomal and deep." },

  /* ---- cardiorespiratory ---- */
  "auscultation": { d: "Listening to breath or heart sounds with a stethoscope to identify added sounds, reduced air entry or abnormal rhythm." },
  "atelectasis": { d: "Collapse of alveoli or a lung segment, reducing gas exchange. Common after surgery and responsive to lung volume strategies." },
  "SpO2": { d: "Peripheral oxygen saturation measured by pulse oximetry. Unreliable with poor perfusion, movement, or carbon monoxide." },
  "tidal volume": { d: "The volume of air moved in a single normal breath — roughly 500 ml in an adult at rest." },
  "ACBT": { d: "Active Cycle of Breathing Technique — breathing control, thoracic expansion and forced expiration, cycled to clear secretions." },
  "PEP": { d: "Positive Expiratory Pressure — exhaling against resistance to splint airways open and mobilise secretions." },
  "dyspnoea": { d: "The subjective sensation of breathlessness. Not reliably proportional to oxygen saturation." },

  /* ---- neurological ---- */
  "spasticity": { d: "Velocity-dependent increase in muscle tone from upper motor neuron lesion — faster passive movement meets more resistance." },
  "hemiplegia": { d: "Complete paralysis of one side of the body, usually following stroke or brain injury." },
  "hemiparesis": { d: "Weakness, rather than complete paralysis, of one side of the body." },
  "ataxia": { d: "Impaired coordination of voluntary movement, typically from cerebellar dysfunction. Produces inaccurate, poorly timed movement." },
  "neglect": { d: "Failure to attend to one side of space or body, most often after right hemisphere stroke. Distinct from a visual field loss." },
  "BPPV": { d: "Benign Paroxysmal Positional Vertigo — brief positional vertigo from displaced otoconia in a semicircular canal. Highly treatable." },
  "nystagmus": { d: "Involuntary rhythmic eye movement. Its direction and behaviour help localise vestibular pathology." },

  /* ---- service & regulation ---- */
  "CPD": { d: "Continuing Professional Development. Physiotherapists registered in Australia must complete 20 hours each year and keep a portfolio for five years." },
  "Ahpra": { d: "The Australian Health Practitioner Regulation Agency — administers registration and accreditation for regulated health professions." },
  "scope of practice": { d: "The range of activities a practitioner is educated, competent and authorised to perform." },
  "SUFE": { d: "Slipped Upper Femoral Epiphysis — displacement through the proximal femoral growth plate in adolescents. A must-not-miss cause of hip or knee pain." },
  "RED-S": { d: "Relative Energy Deficiency in Sport — impaired function across multiple systems from low energy availability." },
  "prognosis": { d: "The expected course and outcome of a condition — what you can honestly tell a patient on day one." },

  /* ---- tissue & histology ---- */
  "collagen": { d: "The main structural protein of tendon, ligament, bone and skin. Type I dominates tendon and bone; type II dominates articular cartilage." },
  "tenocyte": { d: "The resident cell of tendon. Produces and maintains collagen and ground substance, and responds to mechanical load." },
  "fibroblast": { d: "The cell that lays down collagen and extracellular matrix during repair. Becomes a myofibroblast during contraction of a healing wound." },
  "extracellular matrix": { d: "The non-cellular scaffold around cells — collagen, elastin, proteoglycans and water. Its composition determines a tissue's mechanical behaviour." },
  "proteoglycan": { d: "A heavily glycosylated protein that binds water in cartilage and tendon, giving the tissue its compressive stiffness." },
  "synovium": { d: "The membrane lining a joint cavity. Produces synovial fluid and is the primary site of inflammation in inflammatory arthritis." },
  "articular cartilage": { d: "The hyaline cartilage covering joint surfaces. Avascular, aneural, and has very limited capacity to heal once damaged." },
  "subchondral bone": { d: "The bone immediately beneath articular cartilage. Richly innervated — a likely pain source in osteoarthritis, where the cartilage itself is not." },
  "enthesis": { d: "The attachment of tendon or ligament to bone. A transitional zone of fibrocartilage, and a common site of overuse pathology." },
  "periosteum": { d: "The vascular, densely innervated membrane covering bone. Highly pain-sensitive, which is why bone stress injury hurts so specifically." },
  "fascia": { d: "Sheets of connective tissue that envelop and separate muscles and organs, transmitting force between them." },
  "sarcomere": { d: "The contractile unit of skeletal muscle. Its length determines how much force a muscle can generate at a given joint angle." },

  /* ---- physiology ---- */
  "motor unit": { d: "A single motor neuron and every muscle fibre it supplies. Force is graded by recruiting more units and firing them faster." },
  "size principle": { d: "Motor units are recruited smallest-first. Heavy or rapid effort is required to recruit the largest, fastest, most trainable units." },
  "muscle spindle": { d: "A stretch receptor inside muscle that senses length and rate of change. The afferent limb of the stretch reflex." },
  "Golgi tendon organ": { d: "A receptor at the musculotendinous junction sensing tension. Inhibits its own muscle when tension is high." },
  "reciprocal inhibition": { d: "Contraction of a muscle is accompanied by reflex inhibition of its antagonist." },
  "stretch-shortening cycle": { d: "A rapid eccentric contraction immediately followed by a concentric one. Stores and returns elastic energy, producing more force than concentric alone." },
  "cross-bridge": { d: "The myosin head binding to actin. Cycling cross-bridges shorten the sarcomere and generate force." },
  "hypertrophy": { d: "Increase in muscle cross-sectional area from added contractile protein. Distinct from early strength gains, which are mostly neural." },
  "atrophy": { d: "Loss of muscle mass from disuse, denervation, ageing or illness. Begins within days of immobilisation." },
  "neuroplasticity": { d: "The nervous system's capacity to reorganise structure and function in response to experience, training or injury. The basis of neurological rehabilitation." },
  "motor learning": { d: "The relatively permanent change in movement capability from practice. Driven by task specificity, repetition and meaningful feedback." },
  "DOMS": { d: "Delayed Onset Muscle Soreness — soreness peaking 24 to 72 hours after unaccustomed eccentric work. Normal, self-limiting, and not tissue damage." },
  "VO2 max": { d: "The maximum rate of oxygen consumption during incremental exercise. The standard measure of aerobic capacity." },
  "lactate threshold": { d: "The exercise intensity at which blood lactate begins rising disproportionately. A strong predictor of endurance performance." },
  "homeostasis": { d: "The maintenance of a stable internal environment. Training works by disturbing it enough to provoke adaptation." },

  /* ---- pathology ---- */
  "inflammation": { d: "The vascular and cellular response to injury — redness, heat, swelling, pain and loss of function. Necessary for repair, harmful when prolonged." },
  "oedema": { d: "Excess fluid in the interstitial space. Limits range, inhibits muscle reflexively, and slows healing if it persists." },
  "fibrosis": { d: "Excess deposition of disorganised collagen during repair, producing stiffness and reduced tissue compliance." },
  "necrosis": { d: "Uncontrolled cell death from injury, with inflammation. Distinct from apoptosis, which is programmed and orderly." },
  "ischaemia": { d: "Inadequate blood supply to a tissue relative to its demand. Produces pain, dysfunction and, if prolonged, infarction." },
  "infarction": { d: "Tissue death caused by loss of blood supply." },
  "tendinopathy": { d: "Persistent tendon pain and loss of function with load. A failed healing response and disorganised matrix, not primarily inflammation — which is why 'tendinitis' is outdated." },
  "degeneration": { d: "Progressive structural deterioration of tissue. Common on imaging in asymptomatic people, so a poor explanation for pain on its own." },
  "osteophyte": { d: "A bony outgrowth at a joint margin, formed in response to altered load. A radiographic feature of osteoarthritis, not a pain source in itself." },
  "subluxation": { d: "Partial, transient loss of joint congruity that reduces spontaneously — distinct from a dislocation, which does not." },
  "dislocation": { d: "Complete loss of contact between joint surfaces, requiring reduction." },
  "avulsion": { d: "A tendon or ligament pulling away taking a fragment of bone with it. More common than mid-substance rupture in skeletally immature patients." },
  "bone stress injury": { d: "A spectrum from stress reaction to stress fracture, caused by load exceeding the bone's capacity to remodel." },
  "osteoporosis": { d: "Reduced bone mineral density and disrupted microarchitecture, raising fracture risk. Responsive to progressive resistance and impact loading." },
  "sarcopenia": { d: "Age-related loss of muscle mass, strength and function. A central driver of frailty, and reversible with resistance training." },
  "contracture": { d: "Fixed shortening of soft tissue limiting passive range. Develops quickly in immobilised or spastic limbs." },
  "heterotopic ossification": { d: "Bone forming in soft tissue where it should not, often after trauma, burns or neurological injury. Presents as rapidly reducing range with a firm end-feel." },
  "compartment syndrome": { d: "Raised pressure within a closed fascial compartment compromising perfusion. Acute compartment syndrome is a surgical emergency." },

  /* ---- healing ---- */
  "haemostasis": { d: "The first phase of healing — vasoconstriction and clot formation, over minutes to hours." },
  "proliferation": { d: "The healing phase from roughly day three to three weeks, where fibroblasts lay down disorganised type III collagen and new vessels form." },
  "remodelling": { d: "The final healing phase, from weeks to over a year, where collagen reorganises along lines of stress and converts from type III to type I. The phase loading most influences." },
  "granulation tissue": { d: "New connective tissue and capillaries formed during proliferation — fragile, and the substrate for later remodelling." },
  "angiogenesis": { d: "Formation of new blood vessels, essential to repair and a feature of tendinopathy where it is often accompanied by nerve ingrowth." },
  "mechanotransduction": { d: "How cells convert mechanical load into biochemical signals that change tissue structure. The reason loading is the primary treatment for tendon and bone." },
  "Wolff's law": { d: "Bone remodels in response to the loads placed on it — strengthening where loaded, weakening where unloaded." },
  "Davis\u2019 law": { d: "The soft-tissue analogue of Wolff's law: connective tissue remodels along the lines of stress applied to it." },
  "SAID principle": { d: "Specific Adaptation to Imposed Demand — tissue adapts to precisely the demand placed on it, which is why rehabilitation must resemble the target task." },

  /* ---- biomechanics ---- */
  "kinetic chain": { d: "The linked segments through which force is transmitted. Closed-chain movements fix the distal segment; open-chain movements leave it free." },
  "moment arm": { d: "The perpendicular distance from a joint axis to a force's line of action. Longer moment arm, more torque for the same force." },
  "torque": { d: "The rotational effect of a force about a joint axis — force multiplied by moment arm." },
  "ground reaction force": { d: "The force the ground exerts back on the body. Peaks at around two to three times body weight in running." },
  "centre of mass": { d: "The point where body mass is evenly distributed. Its position relative to the base of support determines stability." },
  "base of support": { d: "The area beneath and between the points of contact with the ground. A wider base means greater stability but less mobility." },
  "scapulohumeral rhythm": { d: "The coordinated ratio of glenohumeral to scapulothoracic motion during elevation, around 2:1 after the first 30 degrees." },
  "force couple": { d: "Two or more muscles acting in different directions to produce rotation — as the deltoid and rotator cuff do at the shoulder." },
  "viscoelasticity": { d: "Connective tissue behaving as both a viscous fluid and an elastic solid, so its response depends on how fast and how long load is applied." },
  "creep": { d: "Progressive deformation of tissue under sustained constant load. The basis of prolonged stretch and of end-range postural strain." },
  "hysteresis": { d: "Energy lost as heat during a load-unload cycle. Why repeated loading warms and softens connective tissue." }
};

/* ------------------------------------------------------------------ */
/*  matcher                                                            */
/* ------------------------------------------------------------------ */

const GLOSS_SKIP = new Set(["A", "BUTTON", "H1", "H2", "H3", "H4", "H5", "H6",
  "CODE", "PRE", "KBD", "SCRIPT", "STYLE", "INPUT", "TEXTAREA", "SELECT",
  "LABEL", "OPTION", "SVG", "NAV", "TITLE"]);

function glossInit(root) {
  const scope = root || document;
  const terms = Object.keys(GLOSSARY).sort((a, b) => b.length - a.length);
  if (!terms.length) return;

  const esc2 = t => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  /* longest-first alternation, whole words, optional trailing s */
  const re = new RegExp("\\b(" + terms.map(esc2).join("|") + ")(s?)\\b", "i");
  const lower = {};
  terms.forEach(t => { lower[t.toLowerCase()] = t; });

  const seen = new Set();
  const containers = scope.querySelectorAll("p, li, td, dd, .lede, .card p, .gloss-scan");
  const walkers = [];

  containers.forEach(el => {
    if (el.closest("a, button, .menu, .top, .drawer, .foot, .sw-menu")) return;
    walkers.push(el);
  });

  walkers.forEach(el => {
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
      acceptNode(n) {
        if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        let p = n.parentElement;
        while (p && p !== el.parentElement) {
          if (GLOSS_SKIP.has(p.tagName) || p.classList.contains("gl")) return NodeFilter.FILTER_REJECT;
          p = p.parentElement;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    const nodes = [];
    let n;
    while ((n = walker.nextNode())) nodes.push(n);

    nodes.forEach(node => {
      let text = node.nodeValue, m = re.exec(text);
      if (!m) return;
      const frag = document.createDocumentFragment();
      let idx = 0;
      while (m) {
        const whole = m[0], key = lower[m[1].toLowerCase()];
        if (!key || seen.has(key)) {           /* already marked once on this page */
          frag.appendChild(document.createTextNode(text.slice(idx, m.index + whole.length)));
        } else {
          seen.add(key);
          frag.appendChild(document.createTextNode(text.slice(idx, m.index)));
          const mark = document.createElement("span");
          mark.className = "gl";
          mark.tabIndex = 0;
          mark.setAttribute("role", "button");
          mark.setAttribute("aria-label", key + " — definition");
          mark.dataset.term = key;
          mark.textContent = whole;
          frag.appendChild(mark);
        }
        idx = m.index + whole.length;
        text = text;
        re.lastIndex = 0;
        const rest = text.slice(idx);
        const m2 = re.exec(rest);
        if (!m2) break;
        m2.index += idx;
        m = m2;
      }
      frag.appendChild(document.createTextNode(text.slice(idx)));
      node.parentNode.replaceChild(frag, node);
    });
  });

  glossTip();
}

/* ------------------------------------------------------------------ */
/*  tooltip                                                            */
/* ------------------------------------------------------------------ */

function glossTip() {
  if (document.getElementById("glossTip")) return;
  const tip = document.createElement("div");
  tip.id = "glossTip";
  tip.className = "gl-tip";
  tip.setAttribute("role", "tooltip");
  tip.hidden = true;
  document.body.appendChild(tip);

  let openFor = null, hideT = null;

  const place = el => {
    const entry = GLOSSARY[el.dataset.term];
    if (!entry) return;
    tip.innerHTML = '<b>' + el.dataset.term + '</b><p>' + entry.d + '</p>' +
      (entry.s ? '<span class="gl-src">' + entry.s + '</span>' : '');
    tip.hidden = false;
    tip.classList.remove("in");

    const r = el.getBoundingClientRect();
    const tw = Math.min(330, window.innerWidth - 24);
    tip.style.width = tw + "px";
    const th = tip.offsetHeight;

    /* prefer above; flip below if it would clip the top */
    let top = r.top - th - 11;
    let below = false;
    if (top < 8) { top = r.bottom + 11; below = true; }

    let left = r.left + r.width / 2 - tw / 2;
    left = Math.max(12, Math.min(left, window.innerWidth - tw - 12));

    tip.style.top = Math.round(top + window.scrollY) + "px";
    tip.style.left = Math.round(left) + "px";
    tip.classList.toggle("below", below);

    /* arrow tracks the term even when the box has been nudged sideways */
    const ax = Math.max(16, Math.min(r.left + r.width / 2 - left, tw - 16));
    tip.style.setProperty("--ax", ax + "px");

    requestAnimationFrame(() => tip.classList.add("in"));
    openFor = el;
  };

  const hide = () => {
    clearTimeout(hideT);
    hideT = setTimeout(() => {
      tip.classList.remove("in");
      setTimeout(() => { if (!tip.classList.contains("in")) tip.hidden = true; }, 150);
      openFor = null;
    }, 90);
  };
  const keep = () => clearTimeout(hideT);

  document.addEventListener("mouseover", e => {
    const el = e.target.closest(".gl, .gl-link");
    if (el) { keep(); if (openFor !== el) place(el); return; }
    if (e.target.closest("#glossTip")) { keep(); return; }
    if (openFor) hide();
  });
  document.addEventListener("mouseout", e => {
    if (e.target.closest(".gl, .gl-link") || e.target.closest("#glossTip")) hide();
  });

  /* touch and keyboard */
  document.addEventListener("click", e => {
    const el = e.target.closest(".gl");
    if (el) { e.preventDefault(); openFor === el ? (tip.hidden = true, openFor = null) : place(el); }
    else if (e.target.closest(".gl-link")) { tip.hidden = true; tip.classList.remove("in"); openFor = null; }
    else if (!e.target.closest("#glossTip")) { tip.hidden = true; tip.classList.remove("in"); openFor = null; }
  });
  document.addEventListener("focusin", e => {
    const el = e.target.closest(".gl, .gl-link");
    if (el) { keep(); place(el); }
  });
  document.addEventListener("focusout", e => { if (e.target.closest(".gl, .gl-link")) hide(); });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") { tip.hidden = true; tip.classList.remove("in"); openFor = null; }
  });
  window.addEventListener("scroll", () => { if (openFor) place(openFor); }, { passive: true });
  window.addEventListener("resize", () => { if (openFor) place(openFor); });
}

/* ------------------------------------------------------------------ */
/*  links whose own label is a term                                     */
/*  Used by the section pages: an item called "Sarcopenia" or           */
/*  "Compartment syndrome of the forearm" gets the same tooltip         */
/*  without nesting an interactive element inside a link.               */
/* ------------------------------------------------------------------ */

function glossMatchLabel(label) {
  if (!label) return null;
  const l = label.toLowerCase().replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
  if (!l) return null;
  const keys = Object.keys(GLOSSARY);
  /* exact first */
  for (const k of keys) {
    const kk = k.toLowerCase().replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
    if (kk === l) return k;
  }
  /* then the longest contained whole-word term */
  let best = null;
  for (const k of keys) {
    const kk = k.toLowerCase().replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
    if (!kk || kk.length < 5) continue;
    if (new RegExp("\\b" + kk.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "s?\\b").test(l)) {
      if (!best || kk.length > best.len) best = { key: k, len: kk.length };
    }
  }
  return best ? best.key : null;
}

function glossLinks(root) {
  const scope = root || document;
  const els = $$("[data-gterm]", scope);
  let n = 0;
  els.forEach(el => {
    const key = el.getAttribute("data-gterm");
    if (!GLOSSARY[key]) { el.removeAttribute("data-gterm"); return; }
    el.classList.add("gl-link");
    el.dataset.term = key;
    n++;
  });
  if (n) glossTip();
  return n;
}

document.addEventListener("DOMContentLoaded", () => {
  glossInit();
  glossLinks();
});
