from langchain.document_loaders import UnstructuredPDFLoader




def add_embedding_to_vectordatabase(filepath,campain_id,namespace):
    loader = UnstructuredPDFLoader(file_path=filepath)
    data = loader.load()

    file_path = data[0].metadata["source"]
    import os
    file_name = os.path.basename(file_path)

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=2010, chunk_overlap=25)


    splited_text = splitter.split_documents(data)

    keys = []
    for i in range(0, len(splited_text)):

        keys.append({"document_name": file_name,
                     "filepath": file_path,
                     "campain_id": campain_id,
                     "doc": splited_text[i].page_content}
                    )

    from langchain.schema import Document
    goodDocs = []
    for i in range(0, len(keys)):
        goodDocs.append(Document(
            page_content=keys[i]["doc"],
            metadata={"campain_id": keys[i]["campain_id"],
                      "document_name": keys[i]["document_name"],
                      "source": keys[i]["filepath"]}
        ))

    from langchain_community.embeddings import OpenAIEmbeddings
    from pinecone import Pinecone
    client = Pinecone()

    embeddings = OpenAIEmbeddings()

    client.__init__()
    from langchain_community.vectorstores.pinecone import Pinecone
    index = client.Index("mytargetindex")
    vectorstore = Pinecone(index, embedding=embeddings, text_key="text")

    text_to_add = [i.page_content for i in goodDocs]
    meta_data = [i.metadata for i in goodDocs]
    vectorstore.add_texts(texts=text_to_add, metadatas=meta_data,namespace=namespace)
    print("done")

