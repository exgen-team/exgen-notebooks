\# ExGen Notebook Library



A public collection of Jupyter notebooks for data wrangling, GIS-friendly outputs, and repeatable workflow utilities.



\## Contents



\### Data acquisition

\- \[Download\_Data\_NTGS\_GEMIS](notebooks/Download\_Data\_NTGS\_GEMIS.ipynb)  

&nbsp; Download and structure NTGS GEMIS data for downstream processing.



\### Data wrangling and organisation

\- \[Merge\_csv\_files](notebooks/Merge\_csv\_files.ipynb)  

&nbsp; Merge multiple CSVs into a single consolidated dataset.

\- \[OCR\_csv\_files](notebooks/OCR\_csv\_files.ipynb)  

&nbsp; OCR-driven extraction workflows that output structured tables/CSVs.

\- \[Organise-by-Type](notebooks/Organise-by-Type.ipynb)  

&nbsp; Organise files/data outputs by type for cleaner project structure.



\### Drilling and sampling utilities

\- \[Drilling-Data](notebooks/Drilling-Data.ipynb)  

&nbsp; Drillhole data handling and formatting utilities.

\- \[DrillingStats](notebooks/DrillingStats.ipynb)  

&nbsp; Quick stats/QA summaries for drill datasets.

\- \[Surface\_Samples](notebooks/Surface\_Samples.ipynb)  

&nbsp; Surface sample cleanup and prep steps.

\- \[Rocks-Soils-datacleaning](notebooks/Rocks-Soils-datacleaning.ipynb)  

&nbsp; Cleaning routines for rocks and soils datasets.

\- \[Sediments\_Clean](notebooks/Sediments\_Clean.ipynb)  

&nbsp; Cleaning routines for sediment datasets.



\### GIS and integration

\- \[Merge\_NWQLD\_East-West](notebooks/Merge\_NWQLD\_East-West.ipynb)  

&nbsp; Merge/integrate datasets across areas (GIS-ready outputs).

\- \[Risk-Mapping](notebooks/Risk-Mapping.ipynb)  

&nbsp; Risk mapping workflow elements.

\- \[Workflow\_data\_GSQ](notebooks/Workflow\_data\_GSQ.ipynb)  

&nbsp; End-to-end workflow examples for GSQ-style datasets.



\### Conference / analytics

\- \[RIU\_Conference\_1](notebooks/RIU\_Conference\_1.ipynb)  

&nbsp; Conference-related analysis workflow (company/metadata style processing).



\### PDF utilities

\- \[Extract-pages-from-PDFs](notebooks/Extract\_Images\_PDFs/Extract-pages-from-PDFs.ipynb)  

&nbsp; Extract pages from PDFs (useful for splitting reports).

\- \[Merge\_PDFs\_200mb](notebooks/Extract\_Images\_PDFs/Merge\_PDFs\_200mb.ipynb)  

&nbsp; Merge PDFs with size-awareness (e.g., target ~200MB batches).



\## How to run

1\. Open in JupyterLab / Jupyter Notebook.

2\. Run top-to-bottom.

3\. Some notebooks may require local paths or external downloads. If you plan to share broadly, consider replacing hard-coded paths with variables (e.g., `DATA\_DIR`) near the top of each notebook.



\## Notes

\- `.ipynb\_checkpoints/` folders are ignored (not part of the library).

