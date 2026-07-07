from unittest.mock import MagicMock, patch

from aidp.knowledge.connectors.pubmed_connector import PubMedConnector


@patch("urllib.request.urlopen")
def test_pubmed_fetch_literature_provenance(mock_urlopen) -> None:
    # Mock PMIDs response
    mock_esearch_response = MagicMock()
    mock_esearch_response.read.return_value = b'{"esearchresult": {"idlist": ["12345"]}}'

    # Mock Abstracts XML response
    mock_efetch_response = MagicMock()
    mock_efetch_response.read.return_value = b"""
    <PubmedArticleSet>
        <PubmedArticle>
            <MedlineCitation>
                <PMID>12345</PMID>
                <Article>
                    <ArticleTitle>P53 and Cancer</ArticleTitle>
                    <Abstract>
                        <AbstractText>P53 is a tumor suppressor gene.</AbstractText>
                    </Abstract>
                </Article>
            </MedlineCitation>
            <PubmedData>
                <ArticleIdList>
                    <ArticleId IdType="doi">10.1000/xyz</ArticleId>
                </ArticleIdList>
            </PubmedData>
        </PubmedArticle>
    </PubmedArticleSet>
    """

    # Configure the mock to return esearch then efetch responses
    mock_urlopen.side_effect = [
        MagicMock(__enter__=lambda self: mock_esearch_response, __exit__=lambda *args: None),
        MagicMock(__enter__=lambda self: mock_efetch_response, __exit__=lambda *args: None),
    ]

    connector = PubMedConnector()
    entries = connector.fetch_literature_provenance("p53 cancer")

    assert len(entries) == 1
    entry = entries[0]

    assert entry.claim_text == "P53 is a tumor suppressor gene."
    assert entry.source_paper_doi == "10.1000/xyz"
    assert entry.retriever_metadata["connector"] == "PubMedConnector"
    assert entry.retriever_metadata["title"] == "P53 and Cancer"
