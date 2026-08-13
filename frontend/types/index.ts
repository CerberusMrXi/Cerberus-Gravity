export interface AssetNode {
  id: string;
  name: string;
  type?: string;
  gravity?: number;
  criticality?: number;
  privilege_level?: number;
  reachability?: number;
  exposure?: number;
  trust_level?: number;
  business_value?: number;
  node_type?: string;
  [key: string]: unknown;
}

export interface GraphEdge {
  source: string;
  target: string;
  relationship_type?: string;
  trust?: number;
  permission?: string;
  distance?: number;
  confidence?: number;
}

export interface AttackPath {
  nodes: string[];
  distance: number;
  path_gravity: number;
  average_gravity: number;
  max_node_gravity: number;
  privilege_transitions: number;
  average_trust: number;
  risk: number;
  strategic_attraction: number;
  path_efficiency: number;
  confidence: number;
}

export interface GravityWells {
  single_node_wells: { nodes: string[]; max_gravity: number }[];
  multi_node_wells: { nodes: string[]; max_gravity: number; avg_gravity: number }[];
  total_wells: number;
  threshold: number;
}

export interface FullAnalysis {
  dataset: string;
  gravity_map: Record<string, number>;
  influenced_gravity: Record<string, number>;
  gravity_gradients: Record<string, number>;
  centralities: Record<string, Record<string, number>>;
  strategic_criticality: Record<string, number>;
  gravity_wells: GravityWells;
  metrics: {
    gravity_concentration: number;
    gravity_well_density: { count: number; density: number; wells: Record<string, number>; threshold: number };
    attack_surface_entropy: number;
    node_count: number;
    edge_count: number;
  };
  gravity_distribution: Record<string, number>;
  top_gravity_assets: { id: string; name: string; gravity: number }[];
  attack_paths: AttackPath[];
  graph: {
    nodes: AssetNode[];
    edges: GraphEdge[];
    stats: { node_count: number; edge_count: number };
  };
  disclaimer: string;
}

export interface BlastRadius {
  node_id: string;
  node_name: string;
  reachable_count: number;
  reachable_nodes: string[];
  high_privilege_exposed: { id: string; privilege: number; name: string }[];
  critical_assets_exposed: { id: string; criticality: number; gravity: number; name: string }[];
  estimated_paths_through: number;
  blast_score: number;
}

export interface RemediationResult {
  action: string;
  node_id: string;
  before: { gravity: number; blast_score: number; reachable_count: number; critical_exposed: number };
  after: { gravity: number; blast_score: number; reachable_count: number; critical_exposed: number };
  changes: { gravity_pct: number; blast_score_pct: number; reachable_pct: number };
  note: string;
}
