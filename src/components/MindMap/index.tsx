import React, { useState } from 'react';
import styles from './styles.module.css';

interface NodeData {
  label: string;
  children?: NodeData[];
}

interface MindMapProps {
  root: string | NodeData;
  children?: NodeData[];
}

function TreeNode({ node, isRoot = false }: { node: NodeData; isRoot?: boolean }): JSX.Element {
  const [collapsed, setCollapsed] = useState(false);
  const hasChildren = node.children && node.children.length > 0;

  const toggleCollapse = () => {
    if (hasChildren) {
      setCollapsed(!collapsed);
    }
  };

  return (
    <div className={styles.branch}>
      <div
        className={`${styles.node} ${isRoot ? styles.nodeRoot : ''}`}
        onClick={toggleCollapse}
      >
        <span>{node.label}</span>
        {hasChildren && (
          <span style={{ fontSize: '0.8rem', opacity: 0.7 }}>
            {collapsed ? ' [ + ]' : ' [ − ]'}
          </span>
        )}
      </div>

      {hasChildren && !collapsed && (
        <div className={styles.childrenContainer}>
          {node.children!.map((child, idx) => (
            <TreeNode key={idx} node={child} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function MindMap({ root, children }: MindMapProps): JSX.Element {
  // Normalize the input data: either a single root NodeData, or a label + children list.
  const treeRoot: NodeData = typeof root === 'string'
    ? { label: root, children: children || [] }
    : { ...root };

  return (
    <div className={styles.card}>
      <div className={styles.treeContainer}>
        <TreeNode node={treeRoot} isRoot={true} />
      </div>
    </div>
  );
}
