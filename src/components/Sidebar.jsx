import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  const navItems = [
    { name: 'Tableau de bord', path: '/' },
    { name: 'Nouvelle analyse', path: '/upload-image' },
    { name: 'Bibliothèque d\'images', path: '/image-library' },
    { name: 'Mes patients', path: '/patients' },
    { name: 'Historique', path: '/history' },
    { name: 'Statistiques', path: '/stats' },
    { name: 'Paramètres', path: '/settings' },
  ];

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-6">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
            AB
          </div>
          <div>
            <h3 className="font-semibold">Dr. Ahmed Berrada</h3>
            <p className="text-sm text-gray-500">Radiologue</p>
          </div>
        </div>
      </div>
      <nav className="mt-6">
        <ul>
          {navItems.map((item) => (
            <li key={item.name} className="px-6 py-2">
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `block py-2 px-4 rounded-lg transition-colors ${
                    isActive ? 'bg-blue-50 text-blue-600' : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                {item.name}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;