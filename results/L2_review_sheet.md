# L2 human review sheet (for Ruchit)

For each case read the violation statement, then the REVISED text only, and fill in both answers. This is the human check on the automated verifier.

## Case 1: a14_u2_violation_1 (score 1.52 → 3.09)

**Violation statement:** Gas Safety Insight’s user interface provides only binary alerts (safe/unsafe) without detailed explanations or confidence levels and lacks real-time visualization of underlying sensor data or detected anomalies. Maintenance personnel receive terse notifications devoid of contextual information, limiting their ability to effectively oversee AI outputs as the system operates.

**Revised documentation:**

**Article 14**

**1. Human Oversight Measures Built into the System by the Provider**

*Stop mechanism.* Before the system was placed on the market, Norwin Industrial Technologies integrated a hardware-level interrupt: a physical stop button on the system interface console. Risk assessments had identified the need for direct human intervention capability to counter unintended AI behavior or suspected fault conditions. The button isolates the AI module from sensor feeds within 150 milliseconds. Operators can then halt automated monitoring to investigate or engage fallback safety procedures. System state logs are preserved for forensic review.

*Interface status information.* The user interface shows the current binary alert state (safe/unsafe), updated every second, together with minimal status indicators for system health (online/offline) and communication status. It displays no historical trend insights and no sensor data streams.

*Event records.* The deployed software records all alert state transitions with timestamps and processed input hashes, which enables post-event analysis. It does not provide ongoing contextual data during real-time operation.

*Override.* No interactive override of AI outputs is provided beyond disengaging the system with the physical stop button. The system does not offer alternative recommendations or advice.

**2. Information and Training Provided to Human Overseers**

Gas Safety Insight is delivered to deployers with documentation that sets out strict operational parameters. Users are instructed to treat alerts strictly as triggers for immediate safety protocol initiation, without reliance on interpretative or confidence metrics.

The accompanying user manuals describe the system's limitations. They explicitly warn operators of the potential for false positives and undetected anomalies, owing to the system's conservative alert threshold calibration.

Staff training includes modules on the risk of automation bias. Maintenance personnel are instructed to maintain independent verification through standard inspection routines and not to suspend manual monitoring in the absence of alerts. They receive only concise alert notifications indicating system status transitions, and they rely on established operational protocols to investigate and remediate.

**3. Oversight Objectives and Risk Minimization**

The provider implemented oversight-related controls to address risks inherent in automated critical infrastructure monitoring. In the high-risk context of natural gas infrastructure, constraining alerts to binary states and excluding secondary interpretative data is intended to guard indirectly against misinterpretation-based errors. It aims to reduce ambiguity-related delays in operator response that could elevate safety risks, and so to minimize the likelihood of harm from delayed or incorrect operator assessment of AI output.

**4. Interface Design Decisions and Their Basis**

The user interface presents alert outputs as binary indicators (safe/unsafe). It gives no supplementary explanations, confidence metrics, or real-time visualization of sensor data or anomaly detection results. This design was based on user research and on operational constraints identified during development. Maintenance personnel work under potentially hazardous conditions and require clear, actionable signals rather than detailed diagnostic data.

Iterative usability testing involved 75 maintenance professionals across multiple pilot sites. In that testing, 89% of users reported a preference for concise alerts to streamline response procedures, rather than digesting complex, uncertain AI outputs. These findings informed the provider's choice to limit system feedback to discrete alert states, minimizing information overload and cognitive delay in safety-critical interventions.

The binary alert design was selected over probabilistic or explanatory interfaces based on technical feasibility evaluations and operational context analysis. That analysis indicated that rapid binary decisions most effectively reduce response times and exposure to hazards.

No real-time anomaly visualization or interactive data exploration tools were embedded. This is consistent with the provider's risk assessment that such features could encourage over-reliance on AI output or increase cognitive complexity for operators.

**5. Model Architecture and Output Handling**

The system uses a hybrid AI model that combines Gradient Boosted Decision Trees with encoder-only Transformer modules. It processes fused multi-modal sensor inputs and operational logs. The internal model ensembles generate safety hazard predictions at 1-second intervals and translate model decisions into binary outputs exposed via the user interface.

No confidence scores or probabilistic estimates are exposed, by design, to maintain uniform alert semantics and avoid ambiguity in maintenance actions. AI output logs retain richer decision metadata internally for quarterly model audit. This metadata is not made available in deployment interfaces, owing to security and operational policy constraints.

**6. Model Retraining and Data Records**

The system mandates periodic scheduled model retraining on anonymized datasets. These capture diverse operational conditions over a minimum rolling window of 18 months and encompass over 1.2 million sensor measurement sequences. The retraining keeps model calibration consistent with evolving network characteristics and supports reliability in hazard state classification, without exposing raw data to users.

Records relevant to data processing and bias mitigation are maintained internally under the data protection regulations applicable to special categories of information collected for model development and validation. These records include the justification for the necessity of certain anonymized operational datasets, which are used exclusively to detect and correct bias during offline model updates. This material is not accessible to deployed system users.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 2: a12_u2_violation_1 (score 1.84 → 2.96)

**Violation statement:** Gas Safety Insight only triggers logging when a predefined anomaly threshold is exceeded, neglecting to continuously record routine sensor inputs and decision contexts during normal operation periods.

**Revised documentation:**

**Article 12**

**Technical Provisions for Event Logging**

Gas Safety Insight includes a modular event logging subsystem that records events automatically, without operator action, and is designed to operate over the lifetime of the system. Logging is triggered when the system detects an anomalous state that exceeds a statistically derived threshold. The threshold was established through analysis of historical sensor readings and operational conditions.

*Content of each log entry.* Each triggered anomaly produces a data snapshot containing:
- raw sensor vectors;
- intermediate processed features from the GBDT and Transformer models;
- the anomaly score that led to the threshold breach;
- contextual metadata: timestamp, network segment identifiers, and system health indicators.

*Integrity of the record.* Each log entry is cryptographically timestamped and stored in an append-only, tamper-evident architecture. The architecture conforms to industry standards for critical infrastructure audit trails. This supports chain of custody and reproducibility.

*Scope of recording.* Logging is selective rather than continuous. Events that invoke logging are those indicative of potential safety risks, such as deviations predictive of gas leaks, overpressure, or imminent component failure. Routine sensor inputs and normal operational contexts are not logged continuously. Detailed data retention is therefore limited to higher-impact incidents.

**Rationale and Intended Purpose Alignment**

The threshold-triggered strategy balances traceability against the performance and resource demands of high-frequency, real-time sensor environments. It was validated on a dataset of over 15 million sensor records from multiple gas network segments. That validation showed that continuous logging of all sensor data would generate unmanageable data volumes. It would also obscure genuinely consequential anomalies under the high-noise conditions typical of operational gas supply infrastructure.

Detailed logging is restricted to events whose anomaly score exceeds a threshold empirically linked to a 99% probability of representing a true safety risk or relevant operational fault. This ties logging activity to the risk-based triggering concept in Article 12(2)(a): recording situations that present inherent risk or substantial behavioral deviations requiring intervention. It also keeps the audit record focused on actionable safety events and keeps data noise low for operators.

**Support for Post-Market Monitoring and Operational Surveillance**

Each log entry generated during a triggered anomaly event includes the outputs of the hybrid AI models together with the system state indicators needed for post-market evaluation. The recorded data structure allows the decision pathway leading to an alert to be reconstructed in detail. This supports retrospective analysis of model performance and incident causation, ongoing validation and improvement cycles, and the monitoring activities referenced in Article 12(2)(b) and (c).

During normal operation, when readings are below the anomaly threshold, individual decisions are not recorded in the event log. Aggregated system health statistics and performance metrics for these periods are retained in summary form outside the event log. This reflects the system's design intent and operational profile, in which routine logging of all decisions would produce data of limited relevance to risk assessment.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 3: a10_u4_violation_2 (score 2.67 → 3.55)

**Violation statement:** The training data for Insight Proctor Analytics primarily consists of high-resolution, well-lit classroom recordings, failing to include sufficient data from low-light or unconventional exam settings such as remote proctored tests with webcam-only footage. Additionally, a notable fraction of the annotated segments contain unresolved labeling inconsistencies, such as misclassified hand movements not related to cheating attempts.

**Revised documentation:**

**Article 10**

### Data Governance and Management for Training, Validation, and Testing Sets

Insight Proctor Analytics' development follows structured data governance and management procedures tailored to the system's intended use of video-based academic exam proctoring. The sections below follow the structure of Article 10.

### Design Choices and Assumptions (Art. 10(2)(a), (d))

Annotations were constructed on the operational assumption that hand gestures and movements can be directly correlated with potential cheating indicators. Provider investigations tested this assumption and found systematic ambiguity: ordinary non-cheating behaviors, such as note-taking or gesture-based communication with proctors, were occasionally misclassified. This is an intrinsic limitation of the current label schema and reflects the difficulty of distinguishing covert intent from visual cues alone.

In response, the provider incorporated layered model architectures that integrate visual patterns with semantic test metadata. These architectures cross-validate suspicious gestures against concurrent examination context, which mitigates false positives.

### Data Collection, Origin, and Traceability (Art. 10(2)(b))

The core training corpus consists of over 45,000 hours of video footage, primarily from well-lit, high-resolution classroom recordings made in controlled academic settings at European universities and accredited testing centers. The collection was curated under documented ethical sourcing protocols. The video was originally captured for academic integrity monitoring, with explicit consent and legal compliance respecting privacy regulations.

The provider uses data versioning controls and metadata cataloging to maintain traceability from data acquisition through model training, which supports auditability and reproducibility.

### Data Preparation (Art. 10(2)(c))

Preparation included multi-stage annotation workflows in which experienced annotators flagged cheating-related behaviors, such as unauthorized use of electronic devices, surreptitious note passing, and suspicious gestures. Cleaning steps removed corrupted or incomplete video frames and normalized resolution and color balance for uniform model input. The provider ran multiple cycles of dataset refinement.

Exploratory analyses showed that approximately 12% of hand movement instances in annotated segments were misclassified because of ambiguous labeling guidelines. These inconsistencies remain under ongoing review, and a residual proportion of mislabeled instances persists. This is acknowledged as a limitation in the current system performance documentation.

### Availability and Suitability of Data; Relevance, Representativeness, and Completeness (Art. 10(2)(e), 10(3), 10(4))

The training, validation, and testing datasets were assembled to capture relevant behavioral patterns in conventional, supervised exam environments. The data span several European countries. The bulk of it reflects controlled lighting with stationary, multi-camera recordings typical of examination halls.

Statistical audits show that participant gender and age approximate typical higher-education student populations. Other contextual variables, such as exam formats and room layouts, exhibit moderate homogeneity.

Error analysis and performance benchmarks show detection accuracy that is consistently high (above 91% F1 score) within on-scope environmental conditions. Accuracy degrades in low-light or webcam-only scenarios. Data covering low-light environments or alternative test administration modes, such as remote proctoring with standard webcams of varying video quality, is insufficiently represented at less than 3% of the total dataset. This gap affects representativeness relative to emerging remote or hybrid testing modalities. These deviations are documented in the risk assessment reports, with mitigation actions planned through prioritized data acquisition campaigns.

### Bias Examination, Detection, and Mitigation (Art. 10(2)(f), (g))

Bias detection procedures were conducted to assess whether data imbalances might affect protected groups or negatively distort system outputs. No statistically significant discrimination was detected for gender or ethnic groups represented in the datasets, consistent with the provider's predefined fairness indicators.

Limitations relating to lighting conditions and camera angles point to possible environmental biases that could affect detection reliability in less conventional settings. A continuous monitoring framework scans for performance deviations correlated with contextual variables and triggers alerts for dataset enrichment or algorithm update cycles.

### Identification and Management of Data Gaps and Shortcomings (Art. 10(2)(h))

The provider documents two principal gaps.

1. **Underrepresentation of low-light, webcam-only footage** typical of remote proctoring scenarios. This restricts the operational scope of Insight Proctor Analytics and has informed both the communicated system limitations and the user guidance materials. To partially mitigate the gap, the provider is undertaking extended data collection initiatives that use synthetic augmentation techniques and collaboration with remote testing centers to expand the annotation base for these emerging use cases.

2. **Unresolved annotation inconsistencies**, notably in the classification of hand movements unrelated to cheating. These are flagged in the provider's quality control logs. They have led to conservative decision thresholds in the model deployment pipeline that balance sensitivity and specificity. This reduces the likelihood of false accusations, while potential undetected anomalies remain possible. The trade-offs are documented in the system's technical risk and mitigation reports.

### Data Security and Privacy; Special Categories of Data (Art. 10(5))

Insight Proctor Analytics processes video data of students during examinations. It does not employ biometric identification or process special categories of personal data as defined under Regulations (EU) 2016/679 and (EU) 2018/1725. Visual data is processed exclusively for behavior analysis, without extracting biometric modalities such as facial recognition for identification, and without extracting health data.

The provider's data management protocols enforce strict access controls, encryption at rest and in transit, and pseudonymization at annotation stages to protect individual privacy rights. Residual personal data is subject to retention policies aligned with the stated purpose of academic integrity monitoring. It is expunged following project-specific timelines or upon request, in accordance with applicable data protection laws.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 4: a14_u5_violation_1 (score 1.38 → 2.18)

**Violation statement:** The Talent Insight Model’s user interface only shows final ranked lists without offering insights into which elements of a candidate’s profile most influenced their score or ranking, limiting HR managers’ ability to gauge whether the system’s decisions match expectations or detect anomalies. Moreover, the system uses batch processing without live monitoring dashboards, hindering timely human oversight during recruitment cycles.

**Revised documentation:**

**Article 14**

**Human Oversight of the Talent Insight Model (TIM)**

**1. System Overview and Oversight Context**

The Talent Insight Model (TIM) uses a transformer-based encoder-decoder architecture to process unstructured resume and job description texts. It produces aggregated candidate relevance scores and ranked candidate lists for downstream use by HR professionals. Final hiring decisions remain the responsibility of humans.

TIM runs in batch processing cycles, triggered on demand or scheduled at fixed intervals (commonly nightly). A data pipeline ingests newly submitted or updated applications and job ads. The offline batch strategy has no live inference APIs or continuous streaming mechanisms, which simplifies robustness validation and throughput scaling. Oversight is organized around batch cycles, with review points between the generation of results and their finalization.

The system is delivered on the assumption that deployers will establish active oversight frameworks tailored to their organizational context. The allocation of responsibilities between provider and deployer is set out below. It reflects a risk management approach commensurate with the system's operational autonomy and context of use.

**2. Provider-Implemented Oversight Measures**

The provider has established the following measures, integrated at the point of delivery and subject to technical feasibility boundaries:

- **Human decision-making.** TIM outputs are ranked lists and relevance scores for use by HR professionals. Final hiring decisions remain human responsibilities.

- **Understanding capacities and limitations.** The accompanying technical documentation details model scope, typical performance parameters, known limitations (e.g., opaque attribution, latency due to batch processing) and expected error modes. This documentation supports HR professionals in situating output reliability relative to domain expectations.

- **Awareness of automation bias.** The user interface includes explicit disclaimers cautioning against over-reliance on ranked outputs alone. They emphasize the need for human judgment and holistic candidate evaluation, and remind operators that final hiring decisions remain human responsibilities.

- **Traceability and anomaly investigation.** Audit logs capture all batch processing runs, input data versions, timestamped output archives and pipeline configuration snapshots. These support retrospective review of model outputs and data provenance, and are designed to support deployers' detection and investigation of anomalies or unexpected outcomes post-hoc.

- **Override and interruption.** Manual override workflows are available within the deployment environment (outside the provider software scope). HR managers may use them to exclude or reprioritize candidates based on contextual factors unknown to the model. Deployers can suspend or restart processing pipelines before results are finalized. The system does not natively support direct output negation or 'stop' capabilities within batch jobs.

**3. Risk Mitigation Measures Built into the System**

The design incorporates layered quality control procedures aimed at minimizing the risk of erroneous or biased outputs:

- Model training used a dataset of more than 2 million anonymized, EU-sourced job applicant profiles collected over three years.
- Evaluation metrics include precision@10 of 88.3% and recall@10 of 85.7%.
- Demographic parity tests indicate compliance within ±5% variance across gender and age groups.
- Specialized pre-release adversarial testing assessed vulnerabilities to manipulated CV inputs and synthetic candidates, confirming resilience to typical input perturbations.

The system architecture acknowledges that risks related to misinterpretation, automation bias or output anomalies cannot be fully mitigated through provider-side design alone, given the absence of comprehensive transparency tools or live oversight capabilities. The human oversight model therefore anticipates that deployers will implement complementary organizational controls aligned with their internal governance needs, such as user training, procedural review cycles and manual audit processes.

**4. Deployer-Implemented Oversight Measures**

Because TIM operates in batch mode, it has no live monitoring dashboards and no real-time human-in-the-loop intervention points embedded in the user interface or system backend. The provider does not supply continuous live monitoring dashboards or runtime intervention interfaces. HR managers therefore do not have direct, simultaneous visibility into ongoing model inference activities or dynamic output evolution during recruitment cycles. Deployers are instead expected to implement procedural monitoring aligned with batch schedules, including:

- Periodic manual review of ranked outputs in conjunction with HR expertise, to confirm alignment with recruitment policies and ethical standards.

- Integration of secondary, complementary analytic tools that may provide candidate profile insights or discrepancy detection external to the TIM.

- Protocols for halting or recalibrating recruitment cycles when anomalous patterns or output inconsistencies are identified during scheduled batch validations.

This delegation of live oversight functionality supports a separation of responsibilities, while the provider remains focused on delivering a high-performance core ranking engine.

**5. Human-Machine Interface Design Constraints**

The user interface intentionally presents only final ranked lists of candidates, without detailed explanation or attribution of the candidate profile elements influencing individual scores. This design choice was made to streamline user workflows, reduce cognitive load and protect proprietary model internals. It inherently constrains HR managers' ability to interpret or dissect the model's decision rationale. The TIM's architecture and interface also limit granular insight into internal scoring mechanisms and influence factors.

Accordingly, the system does not provide breakpoint-level feature attributions, influence scores or candidate attribute saliency visualizations. No built-in explainability modules or interactive interrogation tools are integrated at the provider's delivery stage.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 5: a14_u3_violation_1 (score 2.13 → 2.91)

**Violation statement:** The Adaptive Learning Outcome Analyzer’s user interface presents aggregated feedback and learning path recommendations without exposing the underlying model confidence scores, uncertainty measures, or intermediate analytic indicators, limiting educators’ ability to meaningfully monitor or challenge the AI’s reasoning.

**Revised documentation:**

**Article 14**

### Design for Human Oversight and Interface Configuration

The Adaptive Learning Outcome Analyzer presents synthesized feedback and learning path recommendations derived from the AI's analysis of student performance data. Educators oversee the system and keep decision-making authority over its outputs.

The interface was designed around the needs of the educators who oversee it. Usability testing with more than 150 education professionals showed that detailed algorithmic transparency at the confidence or uncertainty level did not improve interpretability and instead increased complexity and cognitive load. The interface therefore presents high-level, aggregated insights and interpretable outcome summaries with recommended adaptive curriculum adjustments. It does not expose model internals such as confidence intervals, uncertainty metrics, intermediate analytics or inferential provenance data.

The system uses transformer-based encoder-decoder architectures optimized for combined text and numerical data. The model was trained on a corpus of more than 3 million anonymized student assessments spanning diverse educational contexts, from primary to tertiary levels. The training data incorporates heterogeneous curricular standards and performance distributions to support robust detection of knowledge gaps.

### Measures Addressing Risk Minimization and Oversight Proportionality

The Analyzer is deployed in educational settings where decisions affect learner pathways and pedagogic strategies. Oversight measures are calibrated to the system's autonomy level, which is constrained. The system provides recommendations without automated enforcement of learner progressions, so educators retain decision-making authority.

Pre-market development included simulated scenario testing to identify risks of misinterpretation or over-reliance on AI outputs, including confirmation bias and neglect of context-specific pedagogical factors. The following mitigations are built into the system:

- Aggregated data presentation formats that avoid probabilistic scores which educators might overinterpret.
- Explicit interface cues reminding users that AI outputs are advisory and should be corroborated with educator judgment.
- Contextualization modules that frame recommendations with reference to cohort-level trends rather than individual performance variances alone.

These design choices are intended to minimize risks to learning quality and fairness by preventing inadvertent automation bias and promoting human deliberation.

### Enabling Understanding and Mitigation of Automation Bias

The system provides embedded textual disclaimers and training modules that raise awareness of the advisory nature of AI outputs. During pilot deployments, Meridian Cognition Technologies collected feedback from 200 educators, who consistently appreciated the emphasis on human-in-the-loop decision-making. This feedback guided the final interface design.

The design avoids presenting precise probabilistic or confidence metrics because these can unintentionally lend false objectivity, and it therefore reduces automation bias. To help users interpret outputs without granular statistical detail, the interface uses standardized terminology and color-coded risk levels linked to aggregate learner cohorts. This balances interpretability with simplicity and lets educators contextualize recommendations relative to their own classroom environment.

### Distribution of Oversight Responsibilities and System Provisions

Before deployment, Meridian Cognition Technologies delivers the system with technical documentation describing the analytical methodology, model limitations and proper usage guidelines. Educators also receive guidance on the system's theoretical basis and known constraints to support informed monitoring. The interface does not expose underlying confidence or uncertainty statistics.

Because outputs are recommendations only, educators can disregard them at their discretion. The Analyzer processes data asynchronously and outputs recommendations rather than taking continuous autonomous actions. Its operational design therefore contains no "stop" button or real-time interruption control. Deployers are responsible for integrating operational controls at the deployment level, including manual override capabilities within educational management platforms.

### Documentation of Special Data Processing Justifications

Training and evaluation involved processing special categories of data (e.g., learner disability indicators) strictly to detect performance biases and inform equitable recommendation generation. The rationale and safeguards for this processing are documented in detail, including ethical review outcomes and data minimization protocols. Alternative data sources without sensitive attributes were evaluated but found insufficient to achieve the bias detection objectives with acceptable accuracy. This justification documents why the processing was necessary to uphold the system's fairness and reliability.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 6: a15_u8_violation_2 (score 2.24 → 2.96)

**Violation statement:** Urban Safety Analytics’ system lacks any fallback procedure when faced with inputs that produce conflicting priority scores between the CNN spatial analysis and the LSTM temporal predictor, resulting in indecisive or non-actionable output without alerting dispatch operators of the inconsistency.

**Revised documentation:**

**Article 15**

**Accuracy, Robustness, and Cybersecurity: Design Overview**

The Emergency Dispatch Prioritization Engine uses a dual neural architecture. A Convolutional Neural Network (CNN) analyses spatial data, and a Long Short-Term Memory (LSTM) recurrent neural network forecasts temporal events. Their outputs are fused into composite priority indices.

**Training Data**

- The CNN was trained on over 250,000 geo-referenced sensor images and topographic data samples. These were collected from multiple urban environments over a 24-month period.
- The LSTM was trained on a sequence database of 1.2 million time-stamped incident reports from emergency services, spanning five years.

**Accuracy and Performance Metrics**

Evaluated independently, the CNN achieved a spatial classification accuracy of 87.6% in identifying high-priority incident zones. The LSTM achieved a temporal event sequence prediction accuracy of 84.9%. These figures reflect conditions including urban noise, sensor variance, and irregular incident patterns, as documented in internal benchmark evaluations conducted quarterly.

Performance metrics are declared explicitly in the user manuals and specification sheets accompanying the system:
- For spatial prioritization, the CNN's precision, recall, and F1-score for critical incident detection are specified.
- For the LSTM model, timeline prediction accuracy, precision, and recall are specified.

These declarations are supported by validation on independent test datasets representing the geographic and temporal diversity of typical deployment environments.

**Robustness Testing**

Both models underwent robustness testing against data perturbations simulating sensor noise and time irregularities. The maximum accuracy degradation under adverse conditions was 5%.

**Consistency Throughout the Lifecycle**

- The system is deployed in a cloud-edge hybrid environment.
- Model weights and inference services are updated quarterly, based on new datasets and performance monitoring feedback.
- Continuous monitoring includes drift detection on input data distributions. It also includes alerting when performance falls more than 4% below baseline benchmarks.
- The models do not engage in autonomous online learning during active deployment, which prevents unverified feedback loops.
- Retraining occurs offline with revalidated datasets before redeployment, so inference behavior is static during operational periods.

**Cybersecurity Measures**

- Cryptographic authentication controls and encrypted data channels (TLS 1.3) are embedded between data inputs and model inference modules.
- Role-based access is enforced.
- All input data and model outputs are logged with tamper-evident audit trails.
- Network intrusion detection systems monitor for anomalous access patterns, with automated containment triggered upon detection of suspicious activities.
- Isolation layers prevent unauthorized modification of inference workflows or deployment components.
- Penetration testing against data poisoning, adversarial input attacks, and unauthorized access was performed biannually by accredited external security experts, with no critical vulnerabilities detected.

**AI-Specific Vulnerabilities**

- Data integrity verification is applied to training datasets.
- Model parameters are securely stored with hash-based verification.
- Routine adversarial robustness evaluations include red-team assessments of model susceptibility to perturbed inputs crafted to influence priority outputs. No critical exploitation vectors were revealed in the latest 2023 evaluation cycle.
- Backup snapshots of training data and models are maintained offline to enable recovery from data poisoning incidents.

**Error and Inconsistency Resilience: Current Limitation**

Priority scoring occurs through parallel inference by the CNN and LSTM subsystems, whose outputs are fused into composite priority indices. A conflict is defined as a priority difference above a predefined threshold of 0.3 on a normalized 0–1 scale. When the two models produce conflicting priority scores in this sense, the system currently lacks an automated fallback or arbitration procedure. No alternate computational mechanism, redundancy protocol, or heuristic override is implemented to reconcile such divergences.

The system also does not generate active alerts or flags in the user interface to notify dispatch operators of these discrepancies. In scenarios of conflicting outputs, the final prioritization recommendation may therefore become indecisive or non-actionable without explicit communication to end users.

This is documented as a current limitation. It is recorded in the system's risk register under "conflicting model output handling" and is slated for future mitigation planning.

**Summary of Design Considerations**

- **Accuracy:** The model ensemble demonstrates validated accuracy and consistent performance across heterogeneous urban datasets.
- **Lifecycle controls:** These comprise offline retraining, drift monitoring, and the absence of online learning.
- **Cybersecurity:** Measures cover authentication, encryption, audit trails, intrusion detection, and adversarial and penetration testing.
- **Remaining technical gap:** Resilience to internal conflicts between component outputs is not yet addressed. The absence of fallback or fail-safe arbitration mechanisms leads to silent indecision states, without direct user notification or system-initiated correction. This is documented in internal assessments as affecting operational robustness.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 7: a12_u1_violation_1 (score 1.62 → 2.32)

**Violation statement:** SafeRoute Traffic Monitor only logs events during active system alerts or when manual logging is triggered by operators, rather than maintaining an automatic and comprehensive continuous event log over the system's lifetime.

**Revised documentation:**

**Article 12**

### Logged Event Content and Traceability

The SafeRoute Traffic Monitor automatically records detailed, event-driven logs in two situations:

- **Active system alerts:** when the AI models detect potential high-risk traffic conditions as defined in the risk model following Article 79(1).
- **Manual logging:** when authorized operators in urban traffic management centers initiate it.

Logging is selective and event-driven. The system does not log continuously or comprehensively.

Each logged episode is recorded at a granularity that supports root-cause analysis and post-incident review. Logs include:

- Timestamped alert metadata
- Input sensor arrays
- Network graph states used by the GNN
- Anomaly scores
- Transformer attention weight summaries, where applicable
- Raw sensor inputs, intermediate feature representations, and model confidence scores, captured as data snapshots when the system's risk thresholds are exceeded

Together these allow the detected hazard and the AI's inferential steps to be reconstructed in detail.

### Relevance of Recorded Events to Article 12(2)

- **(a) Identifying risk situations and substantial modification:** Stored logs focus on events where the AI's internal risk assessment suggests a potential system-induced or detected hazard, or where system parameters may have shifted beyond calibrated ranges. This enables identification of situations that could expose vulnerabilities or substantial system modifications.
- **(b) Post-market monitoring:** Event logs are structured to feed into post-market monitoring workflows. They provide data slices representative of the AI's decision-making context, supporting performance validation and ongoing risk analysis.
- **(c) Monitoring of operation:** Logs generated during alert conditions and operator-triggered manual recordings support operational oversight, continuous improvement cycles, and retrospective operational audits.

### Technical Implementation

The SafeRoute architecture integrates an event logging module that interfaces with the alert generation sub-system of the hybrid AI pipeline. Alert generation uses the outputs of two components:

- The Graph Neural Network (GNN), which models dynamic interdependencies within urban road networks.
- The Transformer-based encoder, which fuses heterogeneous sensor data, including vehicle counts, environmental sensor readings, and incident reports.

The manual logging function is exposed through a secure operator interface. Traffic control authorities can use it to trigger logs based on external observations or operational needs.

Logging is restricted to the alert and manual-trigger conditions through policy-enforced system configurations and technical controls.

### Data Governance and Integrity Controls

- **Validation:** The selective logging approach has been validated through adversarial and boundary condition testing to confirm that no critical high-risk events are omitted from recording due to system configuration or operational scenarios.
- **Access control:** Access to the logging interface and data repositories is governed by role-based access control (RBAC) following the principle of least privilege. Only authorized personnel can initiate manual logging or access high-risk event data.
- **Storage integrity:** Event log storage uses encrypted, tamper-evident databases with automated integrity checks.
- **Accountability:** Audit trails are maintained on access to and modification of logs.
- **Retention:** Retention policies are aligned with applicable data protection standards. Logs are retained for a period consistent with operational analysis cycles and regulatory requirements, after which data are securely deleted or anonymized as necessary.

### Design Rationale

The design prioritizes traceability of functionally significant episodes over exhaustive data accumulation. This approach reduces storage costs, controls sensitive data exposure, and maintains manageable data volumes and system performance. It is intended to preserve the capability to reconstruct the context of critical decisions affecting traffic safety.

### Summary

The SafeRoute Traffic Monitor's logging framework is a targeted, event-driven data capture methodology tailored to its safety monitoring role. It records detailed, access-controlled, tamper-evident logs of alert episodes and operator-initiated events, supporting reconstruction of critical decisions, post-market monitoring and operational oversight. It does not perform continuous or comprehensive event logging across the system's operational lifespan.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 8: a12_u6_violation_2 (score 2.71 → 3.38)

**Violation statement:** The system’s logging excludes metadata about ongoing model retraining processes and detected input inconsistencies that could signal a future risk increase, only recording final decisions and outputs.

**Revised documentation:**

**Article 12**

**Logging Architecture and Event Recording**

Contractual Separation Insight automatically records operational events throughout the system's lifetime. Each log entry captures a final decision output and its rationale, as generated by the ensemble of random forest classifiers and large language model components. Every entry contains:

- the timestamp
- the anonymized job or case identifier
- the final contract termination recommendation
- the key policy references cited in the decision

The logging scope is outcome-oriented, and the logged data is limited to stable decision events. Intermediate metadata from ongoing model retraining workflows and runtime input feature validation flags are not recorded. Transient retraining states and detected input inconsistencies therefore do not appear in the logs.

**Traceability of Potential Risk and Substantial Changes (Article 12(2)(a))**

The logs record the final outcomes of model inference and decision synthesis. Every decision carries a timestamp, so assessors can compare periodic output distributions to identify unusual decision patterns or shifts in system behavior.

The system continuously executes integrity checks and monitors input data quality internally. The process-level alerts from these checks are not written to the logs.

Substantial modifications, such as deployment of a new model ensemble iteration or an LLM update, are documented in versioned deployment metadata held in configuration management databases. These records are kept outside the log files, so operational logs and developmental change records remain separate.

**Support for Post-Market Monitoring (Article 12(2)(b))**

For each conclusion delivered to end users, the logs record:

- the final contract termination advice
- the associated confidence score derived from ensemble aggregation
- structured summaries of the labor law references and company policy clauses underpinning the recommendation

These records allow downstream evaluators and compliance teams to audit decision consistency over time and to identify trends indicative of performance drift or legal nonconformity.

Intermediate scoring metrics and detected discrepancies between input data and expected policy formats are not part of the logging scope. These are handled by internal real-time monitoring that operates separately from the recorded logs.

**Monitoring Operational Functioning (Article 12(2)(c))**

The system uses an event-driven logging schema. It records each interaction that results in a closure recommendation, together with system health check events confirming model availability and inference latency, so authorized monitoring entities can follow the system's operation.

Routine system telemetry, covering CPU load, memory consumption and response times, is captured in a dedicated monitoring platform rather than in the logs that store decision outputs. This keeps outcome logs distinct from resource utilization data. The logs are limited to final results and their critical context, which gives a clear audit trail of the system's decisions.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 9: a14_u3_violation_2 (score 1.25 → 1.90)

**Violation statement:** The system is released without any built-in technical controls to detect or flag anomalous assessment outputs under data distribution shifts (e.g., unconventional student responses or novel curricula), and the provider’s documentation vaguely suggests that deployers should “remain vigilant” without specifying enforceable or structured oversight measures.

**Revised documentation:**

**Article 14**

### Oversight Model and Allocation of Responsibility

The Adaptive Learning Outcome Analyzer is a transformer-based encoder-decoder system that processes mixed modalities, including natural language and numeric tabular data, to provide assessment analytics. Its oversight design is transparency-led. The provider gives deployers, primarily educators and institutional analysts, the information, interface views and controls to oversee outputs, and deployers retain discretion over how outputs are used. Human oversight is a critical element of the system, but it is informally structured. It rests on deployer discretion rather than provider-mandated constraints or monitoring frameworks. By design, the system embeds no technical controls for automatic anomaly detection or operational override under distribution shifts.

### Interface and Output Visibility (Art. 14(1), 14(4)(a), 14(4)(c))

The user interface displays detailed learning outcomes, knowledge gap analyses and tailored feedback. Users see raw and aggregated results and can query and filter assessment outputs directly. Standard visualization elements, such as heatmaps and trend lines, help deployers interpret model outputs in context. Each result comes with a confidence score derived from model softmax outputs. These scores are heuristic indicators only, not anomaly detection mechanisms.

The system has no internal technical controls for detecting or flagging anomalous outputs caused by distributional shifts, such as unexpected student responses or novel curricular content. It has no explicit alerting features for atypical or errant model behavior, and no operational tooling for real-time anomaly detection.

### Information Supplied to Overseers (Art. 14(4)(a)–(c))

The system is delivered with reference materials that set out its functional scope and the limitations of its transformer-based analytic models. They state that the models are sensitive to data multiformity, that output confidence is probabilistic, and that inference accuracy depends on data distributions consistent with training conditions. These materials are intended to help deployers interpret results critically.

Interpretation aids include:
- documentation on the model's tokenization and embedding processes;
- illustrative examples of typical versus atypical output patterns;
- guidance on applying model confidence scores in decision-making contexts.

The help documentation cautions against over-reliance on AI-generated feedback and recommends manual verification where output plausibility is uncertain. The system has no mechanism for detecting automation bias beyond these narrative warnings.

### Risk Management and Oversight Recommendations (Art. 14(2), 14(3)(b))

Risk mitigation focuses on informing deployers of the system's operational boundaries rather than enforcing direct intervention. The documentation identifies scenarios where distributional shifts might impair reliability, such as curricula with substantially novel content or unconventional student answer formulations. It advises deployers to exercise continual vigilance over system outputs. It also recommends that human overseers cross-validate AI-generated learning recommendations against established pedagogical standards and educator judgment.

Assessment of risks from misinterpretation or blind reliance on AI feedback is left to deployer-driven protocols. These risks include erosion of educational equity and misalignment with individualized learner needs. The system embeds no structured, enforceable policies or automated safeguards for anomaly detection or bias correction.

### Output Control, Override and Discontinuation (Art. 14(4)(d), 14(4)(e))

Deployers have full control over the use and disposition of AI outputs, with no automated constraints. They can disregard, override or supplement model-generated recommendations within deployed educational workflows. Software-level controls make user actions that modify assessment interpretations or learning path adjustments straightforward, and these actions are logged. The system does not implement automated override suggestions or intervention triggers.

The system operates within software-as-a-service frameworks and continuous data streams. Discontinuing use in an emergency therefore requires deployer administrative action at the infrastructure level. No in-application "stop" button or emergency halt function has been incorporated, and physical stop controls are not applicable. The provider assessed the risk profile as moderate, given that AI outputs are applied in an advisory rather than prescriptive way in educational settings.

### Documentation of Data Processing and Bias Justification (Art. 14(4)(f))

Processing activities involving personal data, including special categories used for bias identification, are documented in line with Regulations (EU) 2016/679 and (EU) 2018/1725. Justifications for processing sensitive data subsets (e.g., learner demographic factors) centre on their use in model training and validation phases, to help understand population-level biases and performance variance. The provider's documentation includes a general rationale that bias detection objectives require access to such data and that alternative data processing approaches would be insufficient.

The system does not enforce real-time bias correction or dynamic adjustment based on this data during live operation. No automated mechanisms or structural safeguards in the deployed system detect or rectify bias outcomes dynamically once in use.

---

These provisions reflect the provider's decision to emphasize transparency and deployer responsibility for oversight. The system does not embed technical controls for automatic anomaly detection or operational overrides under distribution shifts.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no

## Case 10: a14_u2_violation_2 (score 1.45 → 1.98)

**Violation statement:** Gas Safety Insight does not incorporate interfaces or procedures that alert operators when model confidence is low or when anomalies fall outside the typical operational domain, thereby increasing risks during foreseeable misuse such as sensor degradation or spoofing attacks. Operators are not notified of these limitations, reducing the chance to prevent unsafe reliance on inaccurate or misleading system outputs.

**Revised documentation:**

**Article 14**

### System Overview and Intended Operation

Gas Safety Insight is an automated safety monitoring system that combines Gradient Boosted Decision Trees (GBDT) with encoder-only Transformer models. The GBDT components process structured sensor inputs, such as pressure, flow rate, and temperature readings, captured at 1 Hz intervals from over 10,000 distributed network nodes. The Transformer model ingests unstructured operational logs and contextual metadata over rolling 30-minute windows, enabling temporal anomaly pattern detection and identification of fault precursors.

The training data comprises 2 years of historical network operational data, including 2.4 billion individual sensor readings. Benchmark testing on a corpus of 1 million labeled events from five diverse gas networks showed 92.7% recall on known leak scenarios.

The system acts as a passive anomaly detection provider. Active intervention capability sits with the deployer's operational control centers. Human oversight is therefore exercised mainly through the deployer's control-center operators and the deployer's supervisory systems.

### Allocation of Oversight Measures (Art. 14(3))

- **Measures built into the system:** detailed real-time event logs, anomaly detection timestamps, discrete anomaly scores, binary safety alerts, and APIs for integration with external control systems.
- **Measures to be implemented by the deployer:** stop and override controls, alert suppression, and pausing of monitoring through the deployer's SCADA framework and other supervisory systems. Operators are also expected to carry out routine manual sensor validation, cross-reference with legacy safety procedures, and correlate alerts with corroborative manual inspections.

The provider has not embedded direct stop or override controls in the system interface.

### Design of Outputs and Operator Interface

The system outputs discrete anomaly scores and binary safety alerts. This design prioritizes streamlined alert throughput and minimal alarm fatigue, and it builds on operator familiarity with threshold-based alarms. The user interface (UI) presents an anomaly alert when the combined GBDT and Transformer model scores exceed predetermined thresholds.

The following are not provided:
- Provider-engineered confidence metrics or uncertainty quantification layers. The system therefore does not alert operators to low-confidence outputs or to indications of out-of-distribution anomalies.
- Confidence intervals or anomaly magnitude indicators in outputs.
- Interpretability tools such as feature importance visualizations or uncertainty heatmaps in the UI.
- Integrated human-machine interface (HMI) components that flag potential sensor degradation, input spoofing, or other misuse scenarios that diverge from the operational domain known during model training and validation.

### Information Provided to Support Operator Understanding (Art. 14(4)(a)–(c))

On delivery, Gas Safety Insight is accompanied by technical documentation describing the model architecture, the training data scope, and the evaluation methodology. The documentation states that confidence metrics and anomaly boundaries are not conveyed through system outputs.

Operator training materials accompany deployment. They document the system's intended operational domain and limitations, and they specifically highlight that the system gives no explicit confidence or anomaly boundary notifications. They advise routine manual sensor validation and cross-referencing with legacy safety procedures.

Operators also receive guidance on the risk of automation bias. This guidance recommends correlating alerts with corroborative manual inspections and staying vigilant for sensor abnormalities that system outputs do not signal.

### Monitoring and Review Support

To support operator oversight of health and safety risks arising from system outputs, the system provides detailed real-time event logs and anomaly detection timestamps for post hoc operator review. These logs include raw sensor readings, model outputs, and standard alert levels. They do not encode degrees of confidence or probabilistic uncertainty.

### Robustness Testing

Norwin Industrial Technologies conducted adversarial scenario testing, including simulated sensor drift and spoofing attacks affecting up to 10% of key input streams. Alert rates changed under these conditions, but the system issued no automated warnings of diminished model reliability.

### Operator Controls and Intervention Possibilities (Art. 14(4)(d)–(e))

The deployment package includes APIs that allow integration with external control systems. Operators can suppress alerts or pause monitoring through external supervisory systems configured by the deployer. The deployer's supervisory control and data acquisition (SCADA) framework acts as the ultimate operational governor and is expected to manage stop and override controls. The standalone UI has no direct override or emergency stop functions.

### Records of Processing

Records of processing activities are maintained in line with Regulation (EU) 2016/679 and include data provenance, sensor metadata, and model update logs. No processing of special categories of personal data occurs, so the related justifications are not applicable.

### Summary

Gas Safety Insight's provider decisions center on anomaly detection through hybrid modeling and on transparency about system scope and limitations. The system excludes built-in real-time confidence notifications and direct intervention controls. Human oversight capabilities depend largely on deployer-implemented operational protocols and external supervisory systems rather than on internal system features.

- [ ] Q1: violation still identifiable from the revised text? yes / no
- [ ] Q2: revised text adds or changes any fact? yes / no
