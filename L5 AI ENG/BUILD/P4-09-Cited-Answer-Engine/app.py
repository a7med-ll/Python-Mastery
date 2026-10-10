import hashlib
import os
import tempfile

import streamlit as st

from rag import (
    classify_evidence,
    create_collection,
    extract_pdf_pages,
    filter_relevant_results,
    generate_embeddings,
    index_chunks,
    paragraph_chunking,
    rerank_results,
    search_qdrant,
)


#---------------------------------------------------------------------------------------------------------
# PAGE CONFIG
#---------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Cited Answer Engine",
    layout="wide"
)


#---------------------------------------------------------------------------------------------------------
# SESSION STATE
#---------------------------------------------------------------------------------------------------------

if "indexed_document_id" not in st.session_state:
    st.session_state.indexed_document_id = None

if "indexed_filename" not in st.session_state:
    st.session_state.indexed_filename = None

if "uploaded_file_hash" not in st.session_state:
    st.session_state.uploaded_file_hash = None


#---------------------------------------------------------------------------------------------------------
# HEADER
#---------------------------------------------------------------------------------------------------------

st.title(
    "Cited Answer Engine"
)

st.write(
    "Upload a PDF, index it, and search for the most relevant cited evidence."
)


#---------------------------------------------------------------------------------------------------------
# PDF UPLOAD
#---------------------------------------------------------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
    accept_multiple_files=False
)


if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    document_id = hashlib.sha256(
        file_bytes
    ).hexdigest()   # --> stable document ID based on PDF content


    # --> uploading a different PDF resets the current indexed state
    if st.session_state.uploaded_file_hash != document_id:

        st.session_state.uploaded_file_hash = document_id
        st.session_state.indexed_document_id = None
        st.session_state.indexed_filename = None


    st.success(
        f"Uploaded: {uploaded_file.name}"
    )


    #-----------------------------------------------------------------------------------------------------
    # INDEX DOCUMENT
    #-----------------------------------------------------------------------------------------------------

    if st.button(
        "Index Document"
    ):

        temp_path = None

        try:

            # --> PyMuPDF needs a real file path, so save upload temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    file_bytes
                )

                temp_path = temp_file.name


            with st.spinner(
                "Indexing document..."
            ):

                # --> extract page text and layout blocks
                pages = extract_pdf_pages(
                    temp_path
                )

                # --> live application uses paragraph-aware chunks
                chunks = paragraph_chunking(
                    pages
                )

                # --> create local embedding for every chunk
                chunks = generate_embeddings(
                    chunks
                )

                # --> ensure Qdrant collection exists
                create_collection()

                # --> save vectors and citation metadata
                index_chunks(
                    chunks,
                    document_id=document_id,
                    filename=uploaded_file.name
                )


            # --> remember which PDF is currently searchable
            st.session_state.indexed_document_id = document_id
            st.session_state.indexed_filename = uploaded_file.name


            st.success(
                f"Indexed {len(chunks)} chunks from {len(pages)} pages."
            )


        finally:

            # --> clean up temporary uploaded PDF
            if temp_path and os.path.exists(temp_path):

                os.unlink(
                    temp_path
                )


#---------------------------------------------------------------------------------------------------------
# SEARCH
#---------------------------------------------------------------------------------------------------------

st.divider()

st.subheader(
    "Search Document"
)


query = st.text_input(
    "Ask a question about the uploaded document",
    placeholder="e.g. What is the current upload limit?"
)


if st.button(
    "Search"
):

    #-----------------------------------------------------------------------------------------------------
    # EMPTY QUERY
    #-----------------------------------------------------------------------------------------------------

    if not query:

        st.warning(
            "Please enter a question."
        )


    #-----------------------------------------------------------------------------------------------------
    # DOCUMENT NOT INDEXED
    #-----------------------------------------------------------------------------------------------------

    elif st.session_state.indexed_document_id is None:

        st.warning(
            "Please upload and index a PDF before searching."
        )


    else:

        with st.spinner(
            "Searching document..."
        ):

            #-------------------------------------------------------------------------------------------------
            # VECTOR RETRIEVAL
            #-------------------------------------------------------------------------------------------------

            results = search_qdrant(
                query,
                document_id=st.session_state.indexed_document_id,
                top_k=10
            )


            #-------------------------------------------------------------------------------------------------
            # RERANK TOP CANDIDATES
            #-------------------------------------------------------------------------------------------------

            reranked_results = rerank_results(
                query,
                results,
                top_k=3
            )


            #-------------------------------------------------------------------------------------------------
            # REMOVE WEAK RESULTS
            #-------------------------------------------------------------------------------------------------

            relevant_results = filter_relevant_results(
                reranked_results
            )


            #-------------------------------------------------------------------------------------------------
            # CHECK EXPLICIT / IMPLICIT PREMISE
            #-------------------------------------------------------------------------------------------------

            evidence_check = classify_evidence(
                query,
                reranked_results,
                top_n=3
            )


        #-----------------------------------------------------------------------------------------------------
        # NOTHING RETRIEVED
        #-----------------------------------------------------------------------------------------------------

        if not reranked_results:

            st.warning(
                "No relevant evidence was found in the indexed document."
            )


        #-----------------------------------------------------------------------------------------------------
        # PREMISE EXISTS BUT DOCUMENT CANNOT VERIFY IT
        #-----------------------------------------------------------------------------------------------------

        elif evidence_check["label"] == "not_enough_evidence":

            st.warning(
                "The indexed document does not provide enough evidence "
                "to verify the premise in this question."
            )

            st.write(
                f"**Claim checked:** {evidence_check['claim']}"
            )


        #-----------------------------------------------------------------------------------------------------
        # NORMAL QUESTION WITH NO STRONG EVIDENCE
        #-----------------------------------------------------------------------------------------------------

        elif (
            evidence_check["label"] == "not_checked"
            and not relevant_results
        ):

            st.warning(
                "No sufficiently relevant evidence was found in the indexed document."
            )


        else:

            #-------------------------------------------------------------------------------------------------
            # CONTRADICTED PREMISE
            #-------------------------------------------------------------------------------------------------

            if evidence_check["label"] == "contradicted":

                st.error(
                    "The premise in the question is contradicted by the document."
                )

                st.write(
                    f"**Claim checked:** {evidence_check['claim']}"
                )

                if evidence_check["evidence_text"]:

                    st.write(
                        f"**Evidence used for verification:** "
                        f"{evidence_check['evidence_text']}"
                    )

                st.caption(
                    f"NLI confidence: {evidence_check['score']:.2%} | "
                    f"Evidence rank: {evidence_check['evidence_rank']}"
                )


            #-------------------------------------------------------------------------------------------------
            # SUPPORTED PREMISE
            #-------------------------------------------------------------------------------------------------

            elif evidence_check["label"] == "supported":

                st.success(
                    "The premise in the question is supported by the document."
                )

                st.write(
                    f"**Claim checked:** {evidence_check['claim']}"
                )

                if evidence_check["evidence_text"]:

                    st.write(
                        f"**Evidence used for verification:** "
                        f"{evidence_check['evidence_text']}"
                    )

                st.caption(
                    f"NLI confidence: {evidence_check['score']:.2%} | "
                    f"Evidence rank: {evidence_check['evidence_rank']}"
                )


            #-------------------------------------------------------------------------------------------------
            # DISPLAY ONLY STRONG EVIDENCE
            #-------------------------------------------------------------------------------------------------

            if relevant_results:

                st.subheader(
                    "Most Relevant Evidence"
                )


                for rank, (result, rerank_score) in enumerate(
                    relevant_results,
                    start=1
                ):

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### Result #{rank}"
                        )


                        # --> citation metadata
                        st.write(
                            f"**Document:** {result.payload['filename']}  |  "
                            f"**Page:** {result.payload['page']}  |  "
                            f"**Chunk:** {result.payload['chunk_id']}"
                        )


                        # --> retrieved evidence text
                        st.write(
                            result.payload["text"]
                        )


                        # --> retrieval diagnostics
                        st.caption(
                            f"Vector score: {result.score:.4f} | "
                            f"Rerank score: {float(rerank_score):.4f}"
                        )