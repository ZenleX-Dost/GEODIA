/**
 * Header component — page title and actions.
 */
import { Bell, Settings } from 'lucide-react';

interface HeaderProps {
  title: string;
}

export default function Header({ title }: HeaderProps) {
  return (
    <header className="header">
      <h2 className="header-title">{title}</h2>
      <div className="header-actions">
        <button className="btn btn-ghost btn-sm" title="Notifications">
          <Bell size={18} />
        </button>
        <button className="btn btn-ghost btn-sm" title="Paramètres">
          <Settings size={18} />
        </button>
      </div>
    </header>
  );
}
