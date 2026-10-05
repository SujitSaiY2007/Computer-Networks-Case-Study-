# Paper Acquisition & Archive Protocol — BACSE203

## Purpose

This phase exists to create a stable, auditable full-text corpus **after** candidate-paper verification and **before** detailed evidence extraction.

The project must not spend effort archiving papers that are later excluded, and later chats must not depend only on abstracts or search-result snippets when full text is legitimately available.

## Position in the workflow

**CHAT 01 — Full-Text Verification & Screening**
→ **CHAT 02A — Paper Acquisition & Archive**
→ **CHAT 02 — Evidence Extraction Matrix**
→ **CHAT 03 — Quality Assessment**
→ subsequent synthesis/experiment/manuscript phases.

CHAT 02A is deliberately labelled **02A** so the established numbering of later phases remains stable while the new acquisition checkpoint is inserted between verification and extraction.

## Objective

For every study retained as a primary study after CHAT 01:

1. Locate the legitimate full-text PDF where available.
2. Prefer the official publisher, DOI landing page, institutional repository, author repository, or another legitimate open-access source.
3. Record the exact access source and access status.
4. Download/store the PDF in the user's private/local research archive when legally permitted.
5. Never bypass paywalls, access controls, DRM, or other publisher restrictions.
6. Never commit copyrighted publisher PDFs to the public GitHub repository.
7. Record papers that require institutional/library access so they are not silently treated as unavailable or excluded.
8. Verify that the downloaded PDF corresponds to the verified bibliographic record.

## Access hierarchy

Use this order where practical:

1. Open-access publisher PDF.
2. Official DOI/publisher page with legitimate full-text access.
3. Institutional repository.
4. Author/research-group repository.
5. Legitimate scholarly full-text service/repository.
6. Institutional/library access for paywalled papers.

Do not use pirated copies or unauthorized mirrors.

## Archive policy

The public repository stores:

- bibliographic metadata;
- DOI;
- official/legitimate access link;
- PDF acquisition status;
- access type;
- verification status;
- local filename convention;
- notes about missing pages, supplementary material, or access problems.

The user's private/local archive stores the actual PDFs.

Recommended local structure:

```text
papers/
├── P001_<short-title>.pdf
├── P002_<short-title>.pdf
├── ...
├── P0XX_<short-title>.pdf
└── PAPER_ACCESS_REGISTER.md
```

The `papers/` PDF directory should **not** be pushed to the public GitHub repository unless a file is clearly licensed for redistribution.

## Required register fields

| Field | Requirement |
|---|---|
| Study ID | Must match the verified evidence matrix |
| Short title | Consistent local filename label |
| Full title | Exact verified title |
| Authors | Verified metadata |
| Year | Verified metadata |
| Venue | Exact journal/conference |
| Publisher | Verified publisher |
| DOI | Verified DOI, if assigned |
| Publication type | Journal / conference / other |
| Primary-study status | Included / supporting / excluded |
| Full-text status | Obtained / institutional access / unavailable |
| PDF source | Publisher / repository / other legitimate source |
| Official link | DOI or publisher URL where appropriate |
| PDF filename | Local archive name |
| PDF-to-record check | Pass / needs review |
| Supplementary files | Available / unavailable / not applicable |
| Notes | Access or integrity issues |

## Completion gate

CHAT 02A is complete only when:

- the retained-study list from CHAT 01 is frozen;
- every retained study has an acquisition-register row;
- every legitimately obtainable PDF has been archived locally;
- every inaccessible paper has a documented access status and legitimate access route;
- each archived PDF has been checked against title/DOI/metadata;
- the public repository contains no unauthorized copyrighted PDFs;
- the extraction chat can work from a stable list of verified full texts and explicit missing-evidence statuses.

## Important evidence rule

Obtaining a PDF does **not** mean the paper is high quality or fully accepted as evidence. Inclusion, quality and extraction remain separate decisions.

Likewise, lack of immediate PDF access does not automatically justify exclusion if the paper otherwise meets eligibility criteria; the access problem must be recorded and resolved through legitimate library/publisher routes where possible.

## Handoff to extraction

Once CHAT 02A is complete, update `project/CHAT_HANDOFF.md` with:

- number of retained primary studies;
- number of PDFs obtained;
- number requiring institutional/library access;
- number legitimately unavailable;
- any metadata/PDF mismatches;
- the exact location/name of the access register;
- unresolved acquisition issues;
- the next continuation prompt for CHAT 02 — Evidence Extraction Matrix.

---
# CHAT 02A Acquisition Register — 5 October 2026

**Status: PARTIAL/BLOCKED — legitimate access mapping completed; local PDF materialization is blocked by the current execution environment.**

The verified 40-study baseline is preserved unchanged. No study was removed or substituted.

### Status definitions
- **OBTAINED** = a legitimate full-text copy was located; local materialization was not necessarily successful.
- **INSTITUTIONAL/LIBRARY ACCESS REQUIRED** = authoritative record located but no legitimate openly accessible full text was verified.
- **LEGITIMATELY UNAVAILABLE** = no legitimate full text located.
- **NEEDS REVIEW** = bibliographic or PDF-to-record discrepancy requiring follow-up.

No paper is claimed as locally archived because the execution environment failed a direct PDF materialization test.

| ID | Short title | Full title | Authors | Year | Venue | Publisher | DOI | Type | Status | Full-text status | Legitimate source | Local filename | PDF check | Supplementary | Notes |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| P001 | In-Depth eBPF Security Tools | An In-Depth Analysis of eBPF-Based System Security Tools in Cloud-Native Environments | Jin Her; Jongseop Kim; Jinwoo Kim; Seungsoo Lee | 2025 | IEEE Access | IEEE | 10.1109/ACCESS.2025.3605432 | Journal | Core | OBTAINED | IEEE Xplore OA/CC source | P001_InDepth-eBPF-Security-Tools.pdf | PASS | Not checked | Local materialization failed |
| P002 | eBPF/XDP Deep Learning IoT | Real-Time eBPF/XDP-Based Deep Learning Framework for Anomaly Traffic Detection in Internet of Things Networks | Shuangxing Liu; K. L. Eddie Law; Zien Zhang; Chan Tong Lam | 2026 | IEEE Internet Computing | IEEE | 10.1109/MIC.2026.3692726 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | IEEE/author record | P002_RealTime-eBPF-XDP-DL-IoT.pdf | PASS | Not checked | No open full text verified |
| P003 | CODAX | eBPF-Based Runtime Detection of Semantic DDoS Attacks in Linux Containers | S. Remya; Manu J. Pillai; B. Niranjan; P. M. Ajith Kumar; K. Merin Shaju; K. Dinoy Raj; Somula Ramasubbareddy; Yongyun Cho | 2025 | IEEE Access | IEEE | 10.1109/ACCESS.2025.3614389 | Journal | Core | OBTAINED | IEEE/author full text; CC BY 4.0 | P003_CODAX.pdf | PASS | Not checked | Local materialization failed |
| P004 | AIoT Resilience Monitoring | Low-Overhead Passive Resilience Monitoring for AIoT Gateways: End-to-End Anomaly Detection via eBPF Timing Traces and Autoencoders | Tsui Peng; Ching-Huang Lin; Yu-Chih Wei; Bo-Chang Chen; Jen-Yu Yeh | 2026 | IEEE Access | IEEE | 10.1109/ACCESS.2026.3685156 | Journal | Supporting | OBTAINED | Author full text; CC BY-NC-ND 4.0 | P004_AIoT-Resilience-Monitoring.pdf | PASS | Not checked | Author version located |
| P005 | DeSFAM | DeSFAM: An Adaptive eBPF and AI-Driven Framework for Securing Cloud Containers in Real Time | Sehar Zehra; Hassan Jamil Syed; Fahad Samad; Ummay Faseeha | 2025 | IEEE Access | IEEE | 10.1109/ACCESS.2025.3592192 | Journal | Core | OBTAINED | Author full text; CC BY 4.0 | P005_DeSFAM.pdf | PASS | Not checked | Local materialization failed |
| P006 | Cryptojacking Containers | Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning | Riyeong Kim; Jeongeun Ryu; Sumin Kim; Soomin Lee; Seongmin Kim | 2025 | Electronics | MDPI | 10.3390/electronics14061208 | Journal | Core | OBTAINED | MDPI full text/PDF | P006_Cryptojacking-Containers.pdf | PASS | Not checked | OA publisher |
| P007 | Cloud-Native eBPF Observability | eBPF: A New Approach to Cloud-Native Observability, Networking and Security for Current (5G) and Future Mobile Networks (6G and Beyond) | Soldani et al. | 2023 | IEEE Access | IEEE | 10.1109/ACCESS.2023.3281480 | Journal | Supporting | OBTAINED | IEEE Xplore OA/CC | P007_CloudNative-eBPF-Observability.pdf | PASS | Not checked | OA publisher |
| P008 | BPFast | BPFast: An eBPF/XDP-based high-performance packet payload inspection system for cloud environments | Myoung-sung You; Jin-Woo Kim; Seungwon Shin; Taejune Park | 2022 | JKIISC | KIISE/KCI | 10.13089/JKIISC.2022.32.2.213 | Journal | Supporting | OBTAINED | KCI record/PDF route | P008_BPFast.pdf | PASS | Not checked | PDF route located |
| P009 | Inter-Container XDP/eBPF | Secure Inter-Container Communications Using XDP/eBPF | Jaehyun Nam; Seungsoo Lee; Phillip Porras; Vinod Yegneswaran; Seungwon Shin | 2022 | IEEE/ACM TNET | IEEE/ACM | 10.1109/TNET.2022.3206781 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | DOI/publisher | P009_InterContainer-XDP-eBPF.pdf | PASS | Not checked | No OA copy verified |
| P010 | Kubernetes eBPF Enforcement | Container Instrumentation and Enforcement System for Runtime Security of Kubernetes Platform with eBPF | Songi Gwak; Thien-Phuc Doan; Souhwan Jung | 2023 | Intelligent Automation & Soft Computing | Tech Science Press | 10.32604/iasc.2023.039565 | Journal | Core | OBTAINED | Publisher full text/PDF | P010_Kubernetes-eBPF-Enforcement.pdf | PASS | Not checked | OA |
| P011 | Kubernetes DoS eBPF | Detection of Denial of Service Attack in Cloud Based Kubernetes Using eBPF | Amin Sadiq; Hassan Jamil Syed; Asad Ahmed Ansari; Ashraf Osman Ibrahim; Manar Alohaly; Muna Elsadig | 2023 | Applied Sciences | MDPI | 10.3390/app13084700 | Journal | Core | OBTAINED | MDPI full text/PDF | P011_Kubernetes-DoS-eBPF.pdf | PASS | Not checked | OA |
| P012 | In-Kernel/User-Space ML | Practicality of in-kernel/user-space packet processing empowered by lightweight neural network and decision tree | Takanori Hara; Masahiro Sasabe | 2024 | Computer Networks | Elsevier | 10.1016/j.comnet.2024.110188 | Journal | Supporting | OBTAINED | ScienceDirect OA/full text | P012_InKernel-UserSpace-ML.pdf | PASS | Not checked | OA/CC |
| P013 | eBPF + ML DDoS IDS | Enhancing intrusion detection against denial of service and distributed denial of service attacks: Leveraging extended Berkeley packet filter and machine learning algorithms | Nemalikanti Anand; Saifulla M A; Pavan Kumar Aakula; Raveendra Babu Ponnuru; Chegireddy Rama Prakasha Reddy | 2025 | IET Communications | Wiley | 10.1049/cmu2.12879 | Journal | Supporting | OBTAINED | Wiley Open Access | P013_eBPF-ML-DDoS-IDS.pdf | PASS | Not checked | OA |
| P014 | In-Kernel Autoencoder IDS | Unsupervised Real-Time In-Kernel Intrusion Detection System Using Autoencoders and eBPF | Hotaka Taguchi; Takanori Hara; Shoji Kasahara | 2026 | IEICE Transactions on Communications | IEICE | 10.23919/transcom.2025EBP3028 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | IEICE/J-STAGE record | P014_InKernel-Autoencoder-IDS.pdf | PASS | Not checked | J-STAGE says restricted access |
| P015 | Linux eBPF LSTM Anomaly | Behavioral Anomaly Detection in Linux Systems using eBPF and LSTM Neural Networks: A Comparative Study with Traditional Machine Learning | Author metadata retained from verified record | 2026 | International Journal of Computer Applications | FCS | 10.5120/ijca502db8d4e336 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | DOI/venue record | P015_Linux-eBPF-LSTM-Anomaly.pdf | PASS | Not checked | Full text not verified |
| P016 | eBPF AdaBoost Container Attacks | A Technique for Accurate Detection of Container Attacks with eBPF and AdaBoost | Hyeonseok Shin; Minjung Jo; Hosang Yoo; Yongwon Lee; Byungchul Tak | 2024 | Journal of The Korea Society of Computer and Information | KSCI/KCI | 10.9708/jksci.2024.29.06.039 | Journal | Core | OBTAINED | KCI PDF route | P016_eBPF-AdaBoost-Container-Attacks.pdf | PASS | Not checked | PDF access exposed |
| P017 | Container File-Access Anomaly | An Abnormal File Access Detection Model for Containers Based on eBPF Listening | Naqin Zhou; Hao Chen; Zeyu Chen; Chao Li; Fan Li | 2026 | Mathematics | MDPI | 10.3390/math14060991 | Journal | Core | OBTAINED | MDPI full text/PDF | P017_Container-FileAccess-Anomaly.pdf | PASS | Not checked | OA |
| P018 | Hybrid Malicious Container Detection | Hybrid Runtime Detection of Malicious Containers Using eBPF | Jeongeun Ryu; Riyeong Kim; Soomin Lee; Sumin Kim; Hyunwoo Choi; Seongmin Kim | 2026 | Computers, Materials & Continua | Tech Science Press | 10.32604/cmc.2025.074871 | Journal | Core | OBTAINED | Publisher/SciOpen PDF | P018_Hybrid-Malicious-Container-Detection.pdf | PASS | Not checked | OA/CC BY |
| P019 | Cordon | Cordon: Enhancing security through kernel-level control in containerized computing environments | Qiqing Deng; Zhen Xu; Qihui Zhou; Yan Zhang | 2025 | Computers & Security | Elsevier | 10.1016/j.cose.2025.104644 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | ScienceDirect record | P019_Cordon.pdf | PASS | Not checked | No OA full text verified |
| P020 | BPFGuard | BPFGuard: Multi-Granularity Container Runtime Mandatory Access Control | Hui Lu; Xiaojiang Du; Dawei Hu; Shen Su; Zhi Tian | 2025 | IEEE Transactions on Cloud Computing | IEEE | 10.1109/TCC.2025.3551838 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | IEEE/author record | P020_BPFGuard.pdf | PASS | Not checked | Author-copy request route only |
| P021 | LSM + eBPF Multi-Container Control | Monitoring and Controlling Internal Container Activity Using LSM + eBPF in a Multi-Container Environment | Yejune Ko; Hyeonseok Kim; Mingyu Jeong; Changhyun Lee; Harksu Lim; Sunghyun Jeon | 2026 | Journal of KIISE | KIISE | 10.5626/JOK.2026.53.1.1 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | KCI record | P021_LSM-eBPF-MultiContainer.pdf | PASS | Not checked | ResearchGate reports no full text |
| P022 | eBPF Container Activity Analysis | eBPF-based Container Activity Analysis System | Jisu Kim; Jaehyun Nam | 2024 | Transactions of KIPS | KIPS/KCI | 10.3745/TKIPS.2024.13.9.404 | Journal | Supporting | OBTAINED | KCI PDF route | P022_eBPF-Container-Activity-Analysis.pdf | PASS | Not checked | PDF route located |
| P023 | Optimus | Optimus: Association-Based Dynamic System Call Filtering for Container Attack Surface Reduction | Seungyong Yang; Brent Byunghoon Kang; Jaehyun Nam | 2024 | Journal of Cloud Computing | Springer Nature | 10.1186/s13677-024-00639-3 | Journal | Supporting | OBTAINED | Springer OA PDF | P023_Optimus.pdf | PASS | Not checked | PDF independently inspected; local download failed |
| P024 | Coda | Coda: Runtime Detection of Application-Layer CPU-Exhaustion DoS Attacks in Containers | Mengqi Zhan; Yang Li; Huiran Yang; Guangxi Yu; Bo Li; Weiping Wang | 2023 | IEEE Transactions on Services Computing | IEEE | 10.1109/TSC.2022.3194266 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | DOI/publisher; DBLP marks closed | P024_Coda.pdf | PASS | Not checked | Library route needed |
| P025 | Hela | Hela: A System Call Restriction Framework for Protecting the Entire Containers Lifecycle | Shaohu Li; Jin Zhou; Xinxin Li; Weizhi Meng; Bei Gong; Jun Hu | 2026 | IEEE Transactions on Cloud Computing | IEEE | 10.1109/TCC.2026.3677796 | Journal | Supporting | OBTAINED | Author full text; CC BY 4.0 | P025_Hela.pdf | PASS | Not checked | Legitimate author copy |
| P026 | BeaCon | BeaCon: Automatic Container Policy Generation Using Environment-Aware Dynamic Analysis | Haney Kang; Eduard Marin; Myoungsung You; Diego Perino; Seungwon Shin; Jinwoo Kim | 2026 | Computers & Security | Elsevier | 10.1016/j.cose.2025.104789 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | ScienceDirect + institutional metadata | P026_BeaCon.pdf | PASS | Not checked | No open PDF verified |
| P027 | Vaccine | Vaccine: Injection vulnerabilities mitigation through dynamic process control with eBPF | Author metadata retained from verified publisher record | 2026 | Computers & Security | Elsevier | 10.1016/j.cose.2025.104788 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | ScienceDirect record | P027_Vaccine.pdf | PASS | Not checked | No open PDF verified |
| P028 | Kubernetes IP Spoofing | Preventing IP Spoofing in Kubernetes Using eBPF | Absar Hussain; Abdul Aziz; Hassan Jamil Syed; Shoaib Raza | 2025 | Computers, Materials & Continua | Tech Science Press | 10.32604/cmc.2025.062628 | Journal | Supporting | OBTAINED | Tech Science open-access PDF | P028_Kubernetes-IP-Spoofing.pdf | PASS | Not checked | CC BY 4.0 |
| P029 | KubeAegis | KubeAegis: A Unified Security Policy Management Framework for Containerized Environments | Bom Kim; Seungsoo Lee | 2024 | IEEE Access | IEEE | 10.1109/ACCESS.2024.3487990 | Journal | Supporting | OBTAINED | Author full text; CC BY-NC-ND | P029_KubeAegis.pdf | PASS | Not checked | Legitimate author copy |
| P030 | KubeRosy | KubeRosy: A Dynamic System Call Filtering Framework for Containers | Jin Her; Chi Hyeon Jo; Taejune Park; Seungsoo Lee | 2024 | IEEE Access | IEEE | 10.1109/ACCESS.2024.3486772 | Journal | Supporting | OBTAINED | Author full text; CC BY-NC-ND | P030_KubeRosy.pdf | PASS | Not checked | Legitimate author copy |
| P031 | ML Kernel-Tracing Container Security | Enhancing Container Security Using Machine Learning Based on Kernel Tracing Logs | Author metadata retained from verified publisher record | 2024 | Journal of KIISE | KIISE | 10.5626/JOK.2024.51.11.947 | Journal | Core | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | KCI metadata record | P031_ML-KernelTracing-Container-Security.pdf | PASS | Not checked | Full PDF not verified |
| P032 | Kunerva | Kunerva: Automated Network Policy Discovery Framework for Containers | Seungsoo Lee; Jaehyun Nam | 2023 | IEEE Access | IEEE | 10.1109/ACCESS.2023.3310281 | Journal | Supporting | OBTAINED | Author full text; CC BY-NC-ND | P032_Kunerva.pdf | PASS | Code repository located | Legitimate author copy |
| P033 | Container-to-Cluster Escape | From Container to Cluster: Chained Escape Attacks in Kubernetes and Orchestration Platforms | Jia-Ning Luo; Wen-Han Zou; Shih-Wei Huang | 2025 | IEEE Access | IEEE | 10.1109/ACCESS.2025.3627543 | Journal | Supporting | OBTAINED | IEEE/DBLP open-access route | P033_Container-to-Cluster-Escape.pdf | PASS | Not checked | Open-access record |
| P034 | Lateral-Movement Service Mesh | Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks | Geonwoo Yoon et al. | 2026 | IEEE Transactions on Cloud Computing | IEEE | 10.1109/TCC.2026.3657486 | Journal | Core | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | IEEE Xplore publisher record | P034_LateralMovement-ServiceMesh.pdf | PASS | Not checked | Replacement study; no local PDF |
| P035 | eBPF Network Functions | A Framework for eBPF-Based Network Functions in an Era of Microservices | Stefano Miano; Raffaele Doriguzzi-Corin; Fulvio Risso; Davide Siracusa; Riccardo Sommese | 2021 | IEEE TNSM | IEEE | 10.1109/TNSM.2021.3055676 | Journal | Supporting | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | DOI/publisher record | P035_eBPF-Network-Functions.pdf | PASS | Not checked | No OA PDF verified |
| P036 | ESX | ESX: A Self-Generated Control Policy for Remote Access With SSH Based on eBPF | Yuan Zhong; Pengfei Chen; Huxing Zhang | 2024 | IEEE Access | IEEE | 10.1109/ACCESS.2024.3450496 | Journal | Supporting | OBTAINED | Author full text; CC BY-NC-ND | P036_ESX.pdf | PASS | Not checked | Legitimate author copy |
| P037 | Secure Namespaced Kernel Audit | Secure Namespaced Kernel Audit for Containers | Soo Yee Lim; Bogdan Stelea; Xueyuan Han; Thomas Pasquier | 2021 | ACM SoCC '21 | ACM | 10.1145/3472883.3486976 | Conference | Core | INSTITUTIONAL/LIBRARY ACCESS REQUIRED | ACM/SoCC record; author copy located | P037_Secure-Namespaced-Kernel-Audit.pdf | PASS | Deferred | No local PDF |
| P038 | Malware Detection Cloud Native | Malware Detection in Cloud Native Environments | Brian S. Mitchell; Ansh Chandnani; John Carter; Danai Roumelioti; Spiros Mancoridis | 2024 | AICCC 2024 | ACM | 10.1145/3719384.3719465 | Conference | Core | OBTAINED | Drexel institutional PDF; CC BY 4.0 | P038_Malware-Detection-Cloud-Native.pdf | PASS | Not checked | Legitimate institutional PDF |
| P039 | Cross-Container Attacks | Cross Container Attacks: The Bewildered eBPF on Clouds | Yi He; Roland Guo; Yunlong Xing; Xijia Che; Kun Sun; Zhuotao Liu; Ke Xu; Qi Li | 2023 | USENIX Security '23 | USENIX | — | Conference | Supporting | OBTAINED | Official USENIX PDF | P039_Cross-Container-Attacks.pdf | PASS | Code repo located | Official unrestricted PDF |
| P040 | Kubernetes Runtime Tool Comparison | Comparative Analysis of eBPF-Based Runtime Security Monitoring Tools in Monitoring and Threat Detection on Kubernetes | Aldien Asy Syairozi; Arizal | 2025 | RITECH | SCITEPRESS | 10.5220/0014272700004928 | Conference | Supporting | OBTAINED | SCITEPRESS paper page | P040_Kubernetes-eBPF-Tool-Comparison.pdf | PASS | Not checked | Publisher full-text route |

## CHAT 02A acquisition findings

- **40/40** retained studies have register rows.
- **No study was excluded or substituted because of access difficulty.**
- No pirated copy or unauthorized mirror was used.
- No DOI/title mismatch requiring a screening correction was discovered.
- Supplementary material status remains **Not checked** unless specifically exposed by the source.
- The direct attempt to materialize an openly accessible Springer PDF into the local archive failed. Therefore local archival completion is not claimed.
- The 36-journal + 4-conference composition remains unchanged.
- The project must not enter detailed extraction until the private/local corpus is materialized or legitimate institutional access is used for the remaining papers.

## Completion gate

- [x] Verified 40-study baseline preserved.
- [x] Every retained study has an acquisition-register row.
- [x] Legitimate access route recorded.
- [ ] Every obtainable PDF archived locally — BLOCKED by environment.
- [x] Inaccessible papers explicitly marked.
- [x] Located full texts checked against bibliographic records where accessible.
- [x] No unauthorized PDFs committed to GitHub.
- [x] Repository records the acquisition state.
- [ ] Stable private local PDF corpus ready for CHAT 02 — NOT YET.

**CHAT 02A status: PARTIAL/BLOCKED.**


## CHAT 02 corpus verification checkpoint — 5 October 2026

A direct verification was performed before evidence extraction:

- Mounted local workspace: **0 retained P001–P040 PDFs found**.
- Connected Library search: **no retained study PDFs surfaced**.
- Therefore the existing “OBTAINED” status must continue to mean **legitimate full-text route located**, not **local PDF materialized**.
- Institutional/library-access records remain unresolved for: **P002, P009, P014, P015, P019, P020, P021, P024, P026, P027, P031, P034, P035, P037**.
- No study was excluded because of access difficulty.

**CHAT 02 corpus gate: NOT PASSED.** Evidence extraction must wait until authoritative full text is legitimately available. Do not use “Not reported” for a field that has not yet been inspected in the authoritative full text.
