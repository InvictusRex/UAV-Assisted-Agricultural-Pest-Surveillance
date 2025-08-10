# UAV-Assisted Agricultural Pest Surveillance - Literature Review & Patent Survey

## Executive summary

This document consolidates the most relevant academic contributions and patent filings pertaining to detection of insect pests using unmanned aerial systems (UAS/UAV) and remote sensing. Each work is summarized with an emphasis on the technical approach (model architecture, preprocessing, loss/optimization, sensor modality, dataset characteristics, and reported metrics), followed by a concise critical appraisal that highlights constraints and opportunities for extension. The goal is to provide sufficient technical grounding to (a) reproduce or compare prior art, and (b) identify concrete novelty vectors suitable for algorithmic refinement and intellectual-property protection.

---

## Table of contents

1. Key datasets (summary)
2. Paper summaries (technical)
   1. Bai et al., _A Lightweight Pest Detection Model for Drones …_ (Agriculture, 2023)
   2. _Advanced Insect Detection Network (AIDN) for UAV-Based Biodiversity Monitoring_ (Remote Sensing, 2024)
   3. Alsadik et al., _Remote Sensing Technologies Using UAVs for Pest and Disease Monitoring_ (Remote Sensing, 2024) — review
   4. Subramanian et al., _Drones in Insect Pest Management_ (Frontiers in Agronomy, 2021) — review
   5. _A Framework for Agricultural Pest and Disease Monitoring Based on IoT and UAVs_ (PMC) — systems review
   6. Nasim et al., _Artificial intelligence driven drone observation and pest control in banana crop_ (Khyber Journal, 2025)
   7. Josephat et al., _Design and development of agricultural drone for precision fertilizer application_ (Results in Engineering, 2025)
   8. Safaeinejad et al., _Reducing energy and environmental footprint in agriculture_ (PLOS ONE, 2025)
3. Patent summaries (technical scope & claim emphasis)
   - US 2017/0231213 A1
   - US 2017/0089761 A1
   - US 2022/0211026 A1
   - US 10,364,029 B2
   - WO 2021/196062 A1
   - JP 3217561 U
   - US 11,147,257 B2
   - KR 20230062713 A
4. Comparative analysis: technical gaps and limitations
5. Proposed novelty directions and patentable claim drafts
6. References

---

## 1. Key datasets:

### IP102 (Wang et al. - large insect dataset)

- **Content:** approx. 75k images spanning 102 insect categories (various life stages / viewpoints).
- **Typical use:** classification pretraining, transfer to detection tasks (requires bounding annotations for object detection usage; some community-contributed conversions to YOLO format exist).
- **Limitations for UAV tasks:** largely ground-level or hand-held captures; object scale and background context differ from aerial imagery (scale mismatch).
- **Implication:** recommended as a pretraining resource for feature extraction, followed by domain adaptation (fine-tuning) on aerially collected images.

(See IP102 resources and mirrors on GitHub / Kaggle.)

---

## 2. Paper summaries:

### 2.1 Bai et al. - _A Lightweight Pest Detection Model for Drones Based on Transformer and Super-Resolution Sampling Techniques._ Agriculture (MDPI), 2023.

**Link:** https://www.mdpi.com/2077-0472/13/9/1812

**Objective & context**  
A lightweight detection pipeline was proposed to mitigate the challenge of small pest instances in low-resolution UAV imagery. Emphasis was placed on recovering high-frequency image detail prior to detection and on retaining inference efficiency for edge platforms (Jetson Nano).

**Architectural components**

1. **Super-resolution sampling module (preprocessing):**

   - Implemented as a CNN-based ResNet variant (non-GAN approach) that learns an upsampling mapping by minimising MSE (pixel space).
   - Designed to operate on either whole frames or candidate patches; candidate-region SR is suggested to reduce runtime cost.

2. **Transformer-style detection backbone:**

   - A Transformer-based object detection network was used as the core detector; attention mechanisms are reported to improve discrimination between foreground and heterogeneous backgrounds.
   - The detector accepts super-resolved inputs and outputs bounding boxes + class scores.

3. **Lightweighting methods:**
   - Knowledge distillation, network pruning and quantization techniques were applied to reduce model size for Jetson Nano deployment.

**Training / optimization details**

- **Losses**: standard detection losses (localization + classification) are used; SR module trained with MSE; joint or staged training is discussed, SR as a preprocessing stage with optional joint fine-tuning.
- **Optimizer**: an adaptive optimizer is mentioned; training hyperparameters (batch size, learning rate schedule) are described at a high level in the article.

**Datasets & evaluation**

- The model was evaluated on several pest image datasets and on drone-derived imagery captured with 4K cameras.
- Reported metrics (paper-reported summary): Precision ≈ 0.97, Recall ≈ 0.95, mAP ≈ 0.95, and an inference rate ≈ 57 FPS

**Key takeaways and limitations**

- Super-resolution improved detection metrics for very small instances, but SR introduces computational overhead and potential hallucination of texture that can increase false positives if not regularized.
- The paper demonstrates a pragmatic balance: SR for candidate patches + lightweight detector on Jetson Nano.

---

### 2.2 _Advanced Insect Detection Network (AIDN) for UAV-Based Biodiversity Monitoring._ Remote Sensing (MDPI), 2024.

**Link:** https://www.mdpi.com/2072-4292/17/6/962

**Objective & context**  
AIDN was developed to address the specific constraints of detecting insects in UAV imagery: very small target sizes, high class imbalance, and the need for real-time throughput for field applications.

**Architectural components**

1. **Multi-Scale Feature Fusion (MSFF) module:**

   - Feature maps from multiple backbone layers (denoted F1, F2, F3) are fused via up-sampling and down-sampling pathways; concatenation and convolutional projection follow to yield enriched multi-scale representations.
   - Spatial and channel attention modules are interleaved to emphasize informative signal across scales.

2. **Multi-head detection heads:**

   - Three detection heads operating at different scales (small, medium, large) with kernels (1x1 and 3x3) tuned to optimize the receptive field / localization trade-off for insect sizes (authors report training anchor boxes targeting 10x10 to 30x30 pixel insects in 640x480 input).

3. **Custom loss formulation:**
   - Loss combines localization (IoU-based), classification, and confidence calibration; focal-style weighting or IoU reweighting is applied to counteract class imbalance and tiny target bias.

**Training / optimization**

- Data augmentation emphasizes retaining small object signals (e.g., limited aggressive cropping that can entirely remove tiny objects).
- Anchor box scaling and positive/negative sampling heuristics are adjusted so that small instances are adequately represented during training.

**Datasets & evaluation**

- The authors curated or used aerial insect image sets for evaluation; reported results include mAP ≈ 0.89 on their test sets, precision/recall/F1 scores and real-time throughput claims (e.g., ≈30 FPS on a 15 GFLOPs configuration as reported).

**Key takeaways and limitations**

- AIDN demonstrates that careful multi-scale fusion and loss reweighting materially improve detection of tiny aerial insects.
- The network's computational complexity may limit deployment on strictly constrained embedded devices without further pruning or quantization.
- Generalization to agricultural pest species not present in biodiversity datasets may require additional domain adaptation.

---

### 2.3 Alsadik et al. - _Remote Sensing Technologies Using UAVs for Pest and Disease Monitoring: A Review Centered on Date Palm Trees._ Remote Sensing (MDPI), 2024.

**Link:** https://www.mdpi.com/2072-4292/16/23/4371

**Scope and technical content**

- Comprehensive survey of sensor modalities employed in UAV agricultural applications: RGB, multispectral, hyperspectral, thermal IR, and active sensors (LiDAR). The review includes practical considerations on sensor selection, radiometric/geometric calibration, flight planning (altitude, speed, overlap), and typical data processing pipelines (orthomosaic creation, vegetation indices, anomaly detection).

**Technical observations of relevance**

- **Multispectral/hyperspectral** data facilitate detection of physiological stress via spectral indices (e.g., NDVI, PRI) prior to visual symptoms; spectral signatures can be associated with some pest/disease stressors.
- **Thermal imaging** can reveal canopy temperature anomalies that correlate with infestation or physiological stress, particularly under certain environmental conditions.
- Geometric co-registration of multi-sensor data is non-trivial: the review details calibration/registration techniques and the importance of ground control points (GCPs) when geo-referencing is required.

**Practical constraints noted**

- High-resolution sensors and low flight altitudes increase detection probability for small pests but incur trade-offs with coverage area and flight time.
- Multimodal fusion approaches are encouraged, but few canonical architectures are standardized across studies.

---

### 2.4 Subramanian et al. - _Drones in Insect Pest Management._ Frontiers in Agronomy (2021).

**Link:** https://www.frontiersin.org/articles/10.3389/fagro.2021.640885/full

**Scope and technical content**

- Broad review of UAV applications for pest management: scouting, lure/trap delivery, biological control release, and targeted chemical application. Emphasis is placed on operational constraints (battery life, payload), regulatory considerations, and integration into IPM cycles.

**Key technical points**

- Detection accuracy is highly sensitive to flight altitude and sensor resolution. For pest detection (individual insects), direct detection from standard UAV altitudes is often infeasible unless either: (i) very low altitude flights are performed; or (ii) high-resolution optics and/or super-resolution techniques are applied.
- For many practical use-cases, UAVs are better suited for indirect detection (plant stress indicators) than for direct enumeration of small insects, unless specialized equipment or procedures are used.

---

### 2.5 _A Framework for Agricultural Pest and Disease Monitoring Based on IoT and UAVs._ (PMC review / systems paper)

**Link:** https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7085563/

**Scope and technical content**

- The article proposes an end-to-end framework combining ground IoT sensors, UAV imagery, ML-based image analysis, and decision support systems (DSS). The discussion includes data pipeline structure (collection → preprocessing → feature extraction → model inference → decision rule), and highlights annotation challenges for small targets in agricultural contexts.

**Practical recommendations**

- Strong emphasis on dataset standardization, multimodal annotation reconciliation, and closed-loop decision support integration (alerts, actuation, logging).

---

### 2.6 Nasim et al. - _Artificial intelligence driven drone observation and pest control in banana crop: A systematic review._ Khyber Journal of Medical Research (2025)

**Link:** https://doi.org/10.71146/kjmr197

**Objective & context**

Nasim and colleagues conducted a systematic review exploring the integration of artificial intelligence with drone systems for detecting and managing banana crop diseases. Their work demonstrates how standard leaf imagery can be processed using image classification and machine learning techniques to diagnose diseases and provide treatment recommendations.

**Technical approach**

- The review examines various image classification algorithms applied to banana leaf disease detection, including traditional machine learning approaches and deep learning architectures.
- Focus on developing treatment recommendation systems that guide farmers on appropriate pesticide selection and application timing based on AI-driven disease identification.
- Discussion of smart farming integration where detection systems interface with treatment decision workflows.

**Key findings & implications**

- The study highlights the growing potential of intelligent farming tools that enable early disease detection while providing actionable treatment guidance to farmers.
- Strong emphasis on autonomous systems that can both identify plant diseases and recommend targeted pesticide applications.
- This work provides direct conceptual support for patent applications involving autonomous drones that combine disease identification with targeted spraying capabilities.

---

### 2.7 Josephat et al. - _Design and development of agricultural drone for precision fertilizer application to optimize crop yields._ Results in Engineering (2025)

**Link:** https://doi.org/10.1016/j.rineng.2025.106267

**Objective & context**

Josephat et al. developed a precision agricultural drone specifically designed for efficient fertilizer and pesticide application while minimizing health risks to farmers. The study focuses on practical implementation challenges and system optimization for real-world deployment.

**Technical specifications**

- **Flight control system:** Advanced flight control architecture with PID tuning for spray accuracy and system stability optimization.
- **Spraying mechanism:** Integrated sprayer systems with real-time flow rate control and droplet size management.
- **Monitoring capabilities:** Real-time crop monitoring tools for adaptive application rate adjustment.
- **System integration:** Comprehensive UAV platform designed for large-scale farming operations with emphasis on scalability.

**Performance metrics & validation**

- Demonstrated spray accuracy improvements through PID controller optimization.
- Field testing results showing effective integration into existing farming workflows.
- System stability analysis under various environmental conditions (wind, humidity, temperature variations).

**Key takeaways**

- Provides strong practical evidence supporting the viability of ML-enabled drones for targeted pesticide spraying applications.
- Demonstrates scalability potential for commercial agricultural operations.
- Technical implementation details support patent development for precision spraying systems.

---

### 2.8 Safaeinejad et al. - _Reducing energy and environmental footprint in agriculture: A study on drone spraying vs. conventional methods._ PLOS ONE (2025)

**Link:** https://doi.org/10.1371/journal.pone.0323779

**Objective & context**

Safaeinejad and colleagues conducted a comprehensive comparative analysis examining energy consumption and environmental impact of drone-based pesticide spraying versus conventional tractor-based methods in wheat farming operations.

**Methodology & approach**

- **Life cycle assessment (LCA):** Systematic evaluation of energy consumption and greenhouse gas emissions across the entire operational lifecycle.
- **Comparative analysis:** Direct comparison between UAV-based and traditional tractor-based spraying systems.
- **Environmental impact metrics:** Carbon footprint assessment, energy efficiency calculations, and sustainability indicators.

**Key findings**

- **Energy efficiency:** Drones demonstrated significantly lower energy consumption compared to conventional tractor methods.
- **Environmental benefits:** Reduced greenhouse gas emissions and smaller overall environmental footprint for drone-based systems.
- **Sustainability advantages:** UAV technology offers a more environmentally sustainable alternative to traditional spraying methods.

**Limitations & future considerations**

- **Battery constraints:** Current battery technology limits flight duration and operational range.
- **Training requirements:** Need for specialized operator training presents adoption challenges.
- **Scalability concerns:** Questions remain about deployment across very large agricultural areas.

**Implications for patent development**

- Strong environmental and efficiency justification for drone-based spraying technologies.
- Identifies specific technical challenges (battery life, operational range) that could be addressed in patent claims.
- Supports sustainability arguments for innovative UAV spraying systems.

---

## 3. Patent summaries:

### 3.1 US 2017/0231213 A1 - _Pest Abatement Utilizing an Aerial Drone_

**Link:** https://patents.google.com/patent/US20170231213A1/en

**Claim focus**

- An aerial drone equipped with: (i) pest sensors (chemical/pheromone or camera), (ii) environmental sensors, (iii) an on-board processor to (a) identify pest type (potentially from emissions), (b) estimate risk level, and (c) actuate a pest abatement mechanism (spraying, trapping, nest destruction).
- Several method and system claims describe logic for risk assessment and selection of targeted abatement actions.

**Implications for algorithmic IP**

- The patent primarily claims system/process and hardware integration. It does not appear to claim specific deep-learning architectures for visual detection; however, claims referencing camera-based detection might be broad and should be cleared prior to filing compatible system claims.

---

### 3.2 US 2017/0089761 A1 - _Spectral Imaging System for Remote and Noninvasive Detection_

**Link:** https://patents.google.com/patent/US20170089761A1/en

**Claim focus**

- Hardware and method claims concerning a spectral filter array coupled with an imaging array to detect presence/quantity of target substances using wavelength-selective filters. Processing methods for analyzing spectral bands are claimed (calibration, spectral index computation).

**Implications**

- Strong prior art for multispectral/hyperspectral sensor hardware and signal processing; algorithmic fusion claims involving these modalities should consider scope of this patent when formulating sensor-level claims.

---

### 3.3 US 2022/0211026 A1 - _System and Method for Field Treatment and Monitoring_

**Link:** https://patents.google.com/patent/US20220211026A1/en

**Claim focus**

- System claims covering UAVs and base stations orchestrating field monitoring, data collection, and dispensing workflows; includes logistics, scheduling, and coordination between UAVs and ground assets.

**Implications**

- Claims are system/process oriented; detection algorithm claims that are strictly software/ML-centric may remain outside the narrow scope of these hardware/process patents, though end-to-end system claims coupling detection to actuation will need careful clearance.

---

### 3.4 US 10,364,029 B2 - _Drone for Agriculture (spraying platform)_

**Link:** https://patents.google.com/patent/US10364029B2

**Claim focus**

- Mechanical and electrical design claims for a spraying drone (main frame, nozzle arrays, valving systems, control logic for spray distribution, height sensors). This patent is representative of the large class of agricultural drone hardware patents.

**Implications**

- Hardware actuation claims will be highly encumbered; algorithmic detection and decision-logic claims that simply trigger such hardware are potentially viable but should be crafted to avoid overlap with mechanical/hardware claims.

---

### 3.5 WO 2021/196062 A1 - _Agricultural Drone System for Pest Control_

**Link:** https://patents.google.com/patent/WO2021196062A1/en

**Claim focus**

- International patent application covering an integrated agricultural drone system specifically designed for pest control operations. Claims include flight control mechanisms, pest detection sensors, and targeted application systems for pesticides or biological control agents.
- Method claims describe autonomous flight patterns optimized for crop coverage and pest monitoring workflows.

**Implications**

- Broad international coverage for pest control drone systems; future filings should carefully examine claim scope to identify potential overlaps or opportunities for differentiation through novel detection algorithms or application mechanisms.

---

### 3.6 JP 3217561 U - _Pest Control Drone Utility Model_

**Link:** https://patents.google.com/patent/JP3217561U/en

**Claim focus**

- Japanese utility model focusing on practical design elements of pest control drones including structural configurations, mounting systems for pest control equipment, and user interface components.
- Emphasizes practical implementation aspects rather than algorithmic or software-based innovations.

**Implications**

- Regional protection in Japan for hardware design elements; software and algorithm-focused patent applications may have reduced overlap concerns with this utility model registration.

---

### 3.7 US 11,147,257 B2 - _Autonomous Agricultural System with Pest Detection_

**Link:** https://patents.google.com/patent/US11147257B2/en

**Claim focus**

- Granted patent covering autonomous agricultural systems incorporating pest detection capabilities through sensor arrays and automated response mechanisms.
- Claims include computer vision systems for pest identification, decision-making algorithms for treatment selection, and integration with precision application equipment.
- Method and system claims for coordinating multiple autonomous units in field operations.

**Implications**

- Strong prior art in the autonomous pest detection and treatment space; new applications should focus on novel algorithmic approaches, sensor fusion techniques, or specialized application methods to establish differentiation.

---

### 3.8 KR 20230062713 A - _Smart Pest Control Drone System_

**Link:** https://patents.google.com/patent/KR20230062713A/en

**Claim focus**

- Korean patent application for a smart pest control drone system featuring AI-based pest recognition, automated flight path planning, and precision spraying mechanisms.
- Claims cover integration of machine learning algorithms with drone hardware for real-time pest detection and targeted treatment delivery.

**Implications**

- Recent application indicating active development in this space; demonstrates market interest and competitive landscape evolution. Patent claims should be crafted to highlight specific technical advances beyond general AI integration approaches.

---

## 4. Comparative analysis & Technical gaps

1. **Small-object detection remains the bottleneck.**

   - Prior works have adopted multi-scale fusion, transformer attention, and SR preprocessing. However, few works provide an integrated, reproducible pipeline combining SR, attentioned multimodal fusion (RGB+thermal), and detector co-training optimized specifically for insect-scale instances in aerial imagery.

2. **Multimodal fusion is under-specified.**

   - Reviews recommend multimodal sensing but do not prescribe a canonical fusion architecture for insect detection; this suggests scope for concrete algorithmic inventions (e.g., attention-guided fusion blocks, modality-specific normalization and calibration schemes).

3. **On-device (edge) deployment constraints are addressed at a high level but require further engineering.**

   - Papers propose pruning / knowledge distillation, yet trade-offs between accuracy and latency for specific fusion + SR pipelines are not exhaustively characterized.

4. **Dataset scarcity in the aerial, multimodal domain.**
   - While sizeable insect datasets exist (IP102), matched RGB+thermal aerial datasets with geolocation and per-instance annotations are uncommon, limiting reproducible benchmarking.

5. **Patent landscape shows hardware-focused protection with algorithmic gaps.**

   - Most existing patents emphasize mechanical systems, sensor hardware, and general system integration. Specific algorithmic innovations in multimodal fusion, attention mechanisms, and co-training approaches appear less protected.

6. **Environmental and efficiency advantages are well-documented but implementation challenges remain.**

   - Recent literature strongly supports the environmental benefits of drone-based approaches, but practical deployment obstacles (battery life, operator training, scalability) present opportunities for technical innovation.

---

## 5. Proposed novelty directions (technical details) and illustrative patentable claim outlines

### 5.1 Attention-guided multimodal fusion pipeline (RGB + thermal + NIR)

**Technical specification**

- **Input:** Synchronously captured RGB, thermal, and NIR frames, pre-aligned via a geometric registration module.
- **Per-modality encoders:** Lightweight CNN encoders producing multi-scale feature pyramids for each modality.
- **Super-resolution candidate sampler:** A region proposal module selects candidate boxes with confidence scores; corresponding RGB patches are upsampled by SR module (ResNet-based) to higher resolution and re-encoded.
- **Attention-guided fusion block:** For each scale, fused features are computed where attention weights are spatially computed and normalized across modalities. Channel and spatial attention components are used to emphasize informative signals.
- **Detection head:** YOLO-style multi-scale detection heads operate on fused features to predict bounding boxes and class probabilities.
- **Training objective:** Joint losses combining detection loss (localization + classification + confidence calibration) and SR loss (pixel/perceptual loss for super-resolved patches).

**Rationale for novelty**

- Although SR and multimodal sensing are described in prior literature, the combined pipeline that (i) selectively applies SR to candidate RGB patches, (ii) re-encodes SR outputs, and (iii) fuses multi-scale features via modality-aware attention blocks targeted for insect-scale detection has not been explicitly claimed in the surveyed patents or publications.

**Example method claim**

> A method for detecting insect pests from aerial imagery comprising: receiving aligned RGB, thermal and NIR image frames; generating multi-scale feature pyramids per modality using convolutional encoders; identifying candidate regions using a proposal network and applying super-resolution to candidate RGB patches; re-encoding super-resolved patches and fusing per-scale modality features using spatially-aware attention mechanisms; and predicting bounding boxes and classes using multi-scale detection heads trained with combined detection and reconstruction objectives.

---

### 5.2 Joint SR + detector co-training with candidate-region SR at runtime

**Technical specification**

- SR module and detector are trained jointly where gradient from detection loss back-propagates into SR parameters for candidate regions, encouraging SR to preserve features relevant for detection (e.g., wing venation, body edges, texture patterns).
- Runtime pipeline performs fast inference on low-resolution imagery to obtain high-confidence proposals; only proposals below a size threshold are processed by SR module for enhancement and re-scoring.
- Training employs alternating optimization between SR reconstruction objectives and detection performance metrics.

**Rationale**

- Prior works use SR as preprocessing; co-training SR specifically with detection objectives reduces SR artifacts and focuses reconstruction capacity on discriminative features rather than general image quality.

**Example claim sketch**

> A non-transitory machine readable medium storing instructions that cause a system to: generate initial object proposals from low-resolution aerial imagery; apply a super-resolution model to selected candidate proposals based on size criteria; jointly update both super-resolution and detection model parameters using a combined loss function that includes detection performance metrics and reconstruction quality measures; and deploy the co-trained models for runtime pest detection with selective super-resolution enhancement.

---

### 5.3 Field few-shot fine-tuning workflow (active learning loop)

**Technical specification**

- On a ground station computing device, uncertain detections are presented to an operator in ranked batches based on prediction confidence and spatial clustering.
- The operator provides corrective labels (bounding boxes, class corrections, false positive flags).
- A lightweight fine-tuning routine employing few-shot learning techniques (5-20 gradient steps with strong regularization and data augmentation) updates detector parameters.
- Updated weights are validated on a held-out validation set; if performance improvement exceeds a threshold, the model is deployed to UAV systems or used for batch processing.

**Rationale**

- Integrates practical annotation constraints in field environments while minimizing labeling burden and maximizing detection performance gains through targeted human feedback.

**Example claim sketch**

> A method comprising: identifying low-confidence pest detections from aerial imagery using uncertainty quantification; presenting ranked uncertain detections to human operators for corrective annotation; performing regularized few-shot fine-tuning on a local computing device using the corrective labels; validating performance improvements on held-out data; and conditionally deploying updated model parameters for subsequent aerial pest detection operations.

---

### 5.4 Georeferenced multimodal aerial pest dataset and annotation protocol

**Specification**

- Dataset entries containing: synchronized RGB/thermal/NIR frames with precise timestamps, GPS coordinates, flight altitude, camera intrinsics/extrinsics, and per-instance polygonal annotations with species identification and cross-modal visibility flags.
- Annotation protocol prescribing standardized procedures for reconciling inconsistent modality visibility (e.g., thermal signature present without clear RGB counterpart).
- Quality assurance workflows including inter-annotator agreement metrics and automated consistency checks across modalities.

**Rationale**

- A standardized, well-documented dataset with comprehensive annotation protocols supports reproducible research and provides a defensible intellectual property or licensing asset for training advanced detection systems.

**Claim sketch**

> A computer-readable dataset comprising synchronized multispectral aerial imagery frames and corresponding georeferenced per-instance pest annotations collected according to a defined flight protocol and annotation standard, wherein annotations include cross-modal visibility indicators and species identification metadata.

---

### 5.5 Detection→Decision engine for precision actuation

**Specification**

- Input processing: geotagged detection results with confidence scores, real-time environmental parameters (wind speed/direction, humidity, temperature), and crop phenological stage data.
- Decision algorithms: model-based risk assessment combining pest density mapping, economic threshold calculations, and environmental impact modeling adapted for Integrated Pest Management (IPM) principles.
- Output generation: georeferenced micro-spray instructions including nozzle selection, application rate, flight path optimization, and timing recommendations.

**Rationale**

- While several patents claim dispensing hardware, the specific algorithmic mapping between detection confidence distributions and parametrized environmental decision models may represent novel intellectual property.

**Claim sketch**

> A system for generating precision actuation instructions comprising: receiving georeferenced pest detection data with confidence measures; analyzing environmental parameters including wind conditions and crop development stage; computing treatment recommendations using economic threshold models and environmental impact assessments; and generating georeferenced micro-application commands for deployment to agricultural spraying platforms.

---

## 6. Recommended next steps (technical plan)

1. **Reproduce baseline implementations**
   - Implement baseline YOLOv8/YOLOv11 detector on curated aerial pest dataset (collect 2-3 hours of low-altitude drone video, extract representative frames, perform detailed annotation).

2. **Implement modular SR + candidate-region pipeline**
   - Develop SR module (ResNet-based architecture), integrate with candidate sampling mechanism, and evaluate co-training performance against traditional preprocessing approaches.

3. **Design and implement attention fusion architecture**
   - Prototype modality-specific encoders with spatial/channel attention fusion blocks and quantify mAP improvements on multimodal pilot datasets (RGB+thermal combinations).

4. **Collect comprehensive multimodal dataset**
   - Execute systematic flight missions at optimal altitudes (5-15m) for insect visibility, capture synchronized RGB/thermal recordings with GPS logging and ground control point establishment.
   - Develop annotation protocols for cross-modal instance reconciliation and implement quality assurance workflows.

5. **Performance characterization and ablation studies**
   - Quantify computational requirements (GFLOPs, memory usage), inference speed (FPS) on target hardware platforms (laptop/Jetson devices), and detection performance metrics (mAP, recall) versus RGB-only baseline systems.
   - Document trade-offs between accuracy and computational efficiency to support patent claims and commercial viability assessments.

6. **Patent clearance and filing preparation**
   - Conduct professional patent clearance search focusing on specific algorithmic claims.
   - Prepare provisional patent applications emphasizing novel technical contributions with supporting experimental validation.

---

## 7. References

- Bai, Y., Hou, F., Fan, X., Lin, W., Lu, J., Zhou, J., Fan, D., & Li, L. (2023). _A Lightweight Pest Detection Model for Drones Based on Transformer and Super-Resolution Sampling Techniques._ **Agriculture**, 13(9), 1812. https://doi.org/10.3390/agriculture13091812.

- _Advanced Insect Detection Network (AIDN) for UAV-Based Biodiversity Monitoring._ **Remote Sensing**, 2024. https://www.mdpi.com/2072-4292/17/6/962.

- Alsadik, B., Ellsäßer, F. J., Awawdeh, M., et al. (2024). _Remote Sensing Technologies Using UAVs for Pest and Disease Monitoring: A Review Centered on Date Palm Trees._ **Remote Sensing**, 16(23), 4371. https://doi.org/10.3390/rs16234371.

- Subramanian, K. S., Pazhanivelan, S., Srinivasan, G., et al. (2021). _Drones in Insect Pest Management._ **Frontiers in Agronomy**. https://www.frontiersin.org/articles/10.3389/fagro.2021.640885/full.

- _A Framework for Agricultural Pest and Disease Monitoring Based on IoT and UAVs._ (PMC) https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7085563/

- Nasim, S., Rashid, M., & Yousha, S. (2025). _Artificial intelligence driven drone observation and pest control in banana crop: A systematic review._ **Khyber Journal of Medical Research**, 2(1). https://doi.org/10.71146/kjmr197.

- Josephat, A., Sekar, A., Deepa, T., & Angalaeswari, S. (2025). _Design and development of agricultural drone for precision fertilizer application to optimize crop yields._ **Results in Engineering**, 17, 106267. https://doi.org/10.1016/j.rineng.2025.106267.

- Safaeinejad, M., Ghasemi-Nejad-Raeini, M., & Taki, M. (2025). _Reducing energy and environmental footprint in agriculture: A study on drone spraying vs. conventional methods._ **PLOS ONE**, 20(6). https://doi.org/10.1371/journal.pone.0323779.

**Patents**

- US 2017/0231213 A1 - _Pest Abatement Utilizing an Aerial Drone._ https://patents.google.com/patent/US20170231213A1/en.
- US 2017/0089761 A1 - _Spectral Imaging System for Remote and Noninvasive Detection._ https://patents.google.com/patent/US20170089761A1/en.
- US 2022/0211026 A1 - _System and Method for Field Treatment and Monitoring._ https://patents.google.com/patent/US20220211026A1/en.
- US 10,364,029 B2 - _Drone for Agriculture_ (spraying platform). https://patents.google.com/patent/US10364029B2.
- WO 2021/196062 A1 - _Agricultural Drone System for Pest Control._ https://patents.google.com/patent/WO2021196062A1/en.
- JP 3217561 U - _Pest Control Drone Utility Model._ https://patents.google.com/patent/JP3217561U/en.
- US 11,147,257 B2 - _Autonomous Agricultural System with Pest Detection._ https://patents.google.com/patent/US11147257B2/en.
- KR 20230062713 A - _Smart Pest Control Drone System._ https://patents.google.com/patent/KR20230062713A/en.

---

### Conclusion

The literature and patent landscape analysis reveals significant opportunities for technical innovation in UAV-based agricultural pest surveillance. While existing works have made progress in individual components (super-resolution, attention mechanisms, multimodal sensing), integrated approaches combining these techniques specifically for aerial insect detection remain underexplored. 

The patent landscape shows heavy emphasis on hardware and general system integration, leaving substantial room for algorithmic innovations. Recent literature from 2025 demonstrates growing momentum in this field, with strong evidence supporting both technical feasibility and environmental benefits of drone-based approaches.

A technically rigorous contribution can be advanced through: (i) developing reproducible fusion architectures for multimodal aerial data, (ii) demonstrating quantifiable detection improvements via co-trained SR and attention fusion mechanisms, and (iii) establishing standardized multimodal datasets with comprehensive annotation protocols. 

For formal intellectual property protection, provisional patent applications should focus on concrete algorithmic innovations and system workflows, supported by experimental validation and professional prior art clearance. The identified novelty directions provide a strong foundation for both academic contributions and commercial applications in precision agriculture.
