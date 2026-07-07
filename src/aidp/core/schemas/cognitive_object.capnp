@0xa4cf1762c2f461be;

struct CognitiveObject {
    id @0 :Text;
    documentId @1 :Text;
    pageNumber @2 :Int32;
    paragraphId @3 :Text;
    offsetStart @4 :Int32;
    offsetEnd @5 :Int32;
    chunkIndex @6 :Int32;
    payload @7 :Text;
    timestamp @8 :Float64;
    documentSha256 @9 :Text;
    knowledgeScore @10 :Float64;
}
