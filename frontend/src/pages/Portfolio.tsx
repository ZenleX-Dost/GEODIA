/**
 * Portfolio page — sortable/filterable table of all 19 structures.
 */
import { useEffect, useState } from 'react';
import { Search, ArrowUpDown } from 'lucide-react';
import Header from '../components/layout/Header';
import { getAssets } from '../api/assets';
import type { Ouvrage } from '../types/ouvrage';

const CLASSE_OPTIONS = ['Tous', 'A', 'B', 'C', 'D'] as const;

type SortKey = keyof Pick<Ouvrage, 'code' | 'nom' | 'famille' | 'classe' | 'icf' | 'ivp' | 'ipd' | 'ied'>;

export default function Portfolio() {
  const [assets, setAssets] = useState<Ouvrage[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [classeFilter, setClasseFilter] = useState<string>('Tous');
  const [sortKey, setSortKey] = useState<SortKey>('ipd');
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    getAssets()
      .then(setAssets)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortDir('desc');
    }
  };

  const filtered = assets
    .filter((a) => classeFilter === 'Tous' || a.classe === classeFilter)
    .filter(
      (a) =>
        !search ||
        a.nom.toLowerCase().includes(search.toLowerCase()) ||
        a.code.toLowerCase().includes(search.toLowerCase())
    )
    .sort((a, b) => {
      const aVal = a[sortKey] ?? 0;
      const bVal = b[sortKey] ?? 0;
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return sortDir === 'asc'
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal);
      }
      return sortDir === 'asc'
        ? (aVal as number) - (bVal as number)
        : (bVal as number) - (aVal as number);
    });

  const renderSortIcon = (key: SortKey) => (
    <ArrowUpDown
      size={12}
      style={{
        opacity: sortKey === key ? 1 : 0.3,
        marginLeft: 4,
        display: 'inline',
      }}
    />
  );

  return (
    <>
      <Header title="Portefeuille GC" />
      <main className="app-main">
        <div className="page-container">
          <div className="page-header">
            <h1 className="page-title">Portefeuille d'Ouvrages</h1>
            <p className="page-subtitle">
              19 ouvrages en béton armé — Pôle Industriel de Jorf Lasfar
            </p>
          </div>

          {/* Toolbar */}
          <div className="toolbar">
            <div className="toolbar-left">
              <div className="search-input">
                <Search size={18} />
                <input
                  type="text"
                  placeholder="Rechercher par nom ou code..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
              <div className="filter-chips">
                {CLASSE_OPTIONS.map((c) => (
                  <button
                    key={c}
                    className={`chip ${classeFilter === c ? 'active' : ''}`}
                    onClick={() => setClasseFilter(c)}
                  >
                    {c === 'Tous' ? 'Tous' : `Classe ${c}`}
                  </button>
                ))}
              </div>
            </div>
            <div className="toolbar-right">
              <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-tertiary)' }}>
                {filtered.length} ouvrage{filtered.length > 1 ? 's' : ''}
              </span>
            </div>
          </div>

          {/* Data Table */}
          {loading ? (
            <div className="loading-spinner">
              <div className="spinner" />
            </div>
          ) : (
            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th onClick={() => handleSort('code')}>
                      Code {renderSortIcon('code')}
                    </th>
                    <th onClick={() => handleSort('nom')}>
                      Nom {renderSortIcon('nom')}
                    </th>
                    <th onClick={() => handleSort('famille')}>
                      Famille {renderSortIcon('famille')}
                    </th>
                    <th onClick={() => handleSort('classe')}>
                      Classe {renderSortIcon('classe')}
                    </th>
                    <th onClick={() => handleSort('icf')}>
                      ICF {renderSortIcon('icf')}
                    </th>
                    <th onClick={() => handleSort('ivp')}>
                      IVP {renderSortIcon('ivp')}
                    </th>
                    <th onClick={() => handleSort('ipd')}>
                      IPD {renderSortIcon('ipd')}
                    </th>
                    <th onClick={() => handleSort('ied')}>
                      IED {renderSortIcon('ied')}
                    </th>
                    <th>Exposition</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((asset) => (
                    <tr key={asset.id}>
                      <td>
                        <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                          {asset.code}
                        </span>
                      </td>
                      <td style={{ maxWidth: 300 }}>{asset.nom}</td>
                      <td>
                        <span style={{ textTransform: 'capitalize' }}>
                          {asset.famille}
                        </span>
                      </td>
                      <td>
                        <span className={`badge badge-classe-${asset.classe.toLowerCase()}`}>
                          {asset.classe}
                        </span>
                      </td>
                      <td className="numeric">{asset.icf?.toFixed(1) ?? '—'}</td>
                      <td className="numeric">{asset.ivp?.toFixed(1) ?? '—'}</td>
                      <td className="numeric">
                        <span style={{ fontWeight: 700 }}>
                          {asset.ipd?.toFixed(1) ?? '—'}
                        </span>
                      </td>
                      <td className="numeric">{asset.ied?.toFixed(1) ?? '—'}</td>
                      <td>
                        <span
                          style={{
                            fontFamily: 'var(--font-mono)',
                            fontSize: 'var(--text-xs)',
                            color: 'var(--text-tertiary)',
                          }}
                        >
                          {asset.exposition ?? '—'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </>
  );
}
