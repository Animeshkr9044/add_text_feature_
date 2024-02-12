



def delete_embbeding_from_vectorstore(campain_id):
    from pinecone import Pinecone

    client = Pinecone()
    from langchain_community.embeddings import OpenAIEmbeddings

    embeddings = OpenAIEmbeddings()

    client.__init__()
    from langchain_community.vectorstores.pinecone import Pinecone

    index = client.Index("mytargetindex")
    vectorstore = Pinecone(index, embedding=embeddings, text_key="text")
    # Define filter to find the document by name
    filter = {
        "campain_id": {"$eq": campain_id}
    }

    vectorstore.delete(filter=filter)
    print("done")









