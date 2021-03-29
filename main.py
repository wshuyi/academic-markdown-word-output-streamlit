import streamlit as st 
from io import StringIO
import os
from pathlib import Path
import base64
from zipfile import ZipFile

# write uploaded object to a file
def upl_file_save(upl, fname):
    stringio = StringIO(upl.read().decode("utf-8"))
    with open(fname, 'w') as f:
        f.write(stringio.read())

# filename defs

better_bibtex_json_fname = "better_bibtex_json.json"
markdown_fname = "text.md"
docx_output = "output.docx"
out_docx_zip = "output.zip"
custom_csl_fname = "custom.csl"

csl = None

st.title("Academic Word Doc Exporter")
cite_style = st.radio("Cite Style:", ("GBT7714-2015-number", "APA", "other"))
if cite_style == "GBT7714-2015-number":
    csl = "china-national-standard-gb-t-7714-2015-numeric.csl"
elif cite_style == "APA":
    csl = "apa.csl"
else:
    # other
    custom_csl_upl = st.file_uploader("Upload your Citation Style (csl) file", type=["csl"])
    if custom_csl_upl is not None:
        csl = custom_csl_fname
        upl_file_save(custom_csl_upl, csl)

better_bibtex_json_upl = st.file_uploader("Upload your Better Bibtex JSON file", type=["json"])
markdown_file_upl = st.file_uploader("Upload your Markdown file", type=["md", "markdown"])



if csl:
    # citation style defined already
    if better_bibtex_json_upl is not None and markdown_file_upl is not None:
        # both uploaded
        # generate better_bibtex_json.json
        
        upl_file_save(better_bibtex_json_upl, better_bibtex_json_fname)
        # generate markdown file
        
        upl_file_save(markdown_file_upl, markdown_fname)
        
        # generate docx file
        cmd = f"""
                        pandoc -s --citeproc \
                            --bibliography '{better_bibtex_json_fname}' \
                                --csl '{csl}' \
                                                            --wrap=none \
                    '{markdown_fname}' \
                    -o '{docx_output}' 
                        """
        os.system(cmd)
        # st.write(cmd)

        if Path(docx_output).exists():
            st.write(f"{docx_output} generated!")
            
            with ZipFile(out_docx_zip, "w") as zip:
                zip.write(docx_output)

            with open(out_docx_zip, "rb") as f:
                bytes = f.read()
                b64 = base64.b64encode(bytes).decode()
                href = f'<a href="data:file/zip;base64,{b64}" download=\'{out_docx_zip}\'>\
                    Click to download the zip file\
                </a>'


            # # clean up
            # os.remove(out_json)
            # os.remove(out_json_zip)

                
            st.markdown(href, unsafe_allow_html=True)


if st.button("Clean up all files"):
    cmd = f"rm -f {better_bibtex_json_fname} {markdown_fname} {docx_output} {out_docx_zip} {custom_csl_fname}"
    os.system(cmd)

