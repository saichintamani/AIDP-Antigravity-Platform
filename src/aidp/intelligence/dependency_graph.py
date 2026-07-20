
class CyclicDependencyError(Exception):
    pass

class Node:
    def __init__(self, node_id: str, node_type: str, data: any):
        self.node_id = node_id
        self.node_type = node_type # 'CLAIM' or 'EVIDENCE'
        self.data = data
        self.confidence: float = 1.0
        self.parents: set[str] = set() # Nodes that support this node
        self.children: set[str] = set() # Nodes this node supports

class EvidenceDependencyGraph:
    """
    A Directed Acyclic Graph tracking epistemic support between Evidence and Claims.
    """
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        
    def add_node(self, node_id: str, node_type: str, data: any = None) -> Node:
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, node_type, data)
        return self.nodes[node_id]
        
    def add_edge(self, source_id: str, target_id: str):
        """
        Adds a directed edge source -> target. Meaning 'source' SUPPORTS 'target'.
        Raises CyclicDependencyError if this creates a cycle.
        """
        if source_id not in self.nodes:
            raise ValueError(f"Source node {source_id} does not exist.")
        if target_id not in self.nodes:
            raise ValueError(f"Target node {target_id} does not exist.")
            
        if self._would_create_cycle(source_id, target_id):
            raise CyclicDependencyError(f"Edge {source_id} -> {target_id} creates a cycle.")
            
        self.nodes[source_id].children.add(target_id)
        self.nodes[target_id].parents.add(source_id)
        
    def _would_create_cycle(self, source_id: str, target_id: str) -> bool:
        """
        DFS to detect if adding source -> target creates a cycle.
        A cycle is created if target can reach source.
        """
        if source_id == target_id:
            return True
            
        visited = set()
        stack = [target_id]
        
        while stack:
            curr = stack.pop()
            if curr == source_id:
                return True
            if curr not in visited:
                visited.add(curr)
                stack.extend(self.nodes[curr].children)
                
        return False

    def get_descendants(self, node_id: str) -> list[str]:
        """
        Returns all nodes topologically downstream of the given node.
        """
        if node_id not in self.nodes:
            return []
            
        visited = set()
        stack = list(self.nodes[node_id].children)
        
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                stack.extend(self.nodes[curr].children)
                
        return list(visited)
