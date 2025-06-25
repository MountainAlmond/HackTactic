import React, { useState } from 'react';
import './styles/EntityList.css';

interface Item {
  id: number;
  value: string;
}

interface EntityListProps {
  title: string;
  initialItems: Item[];
}

export const EntityList: React.FC<EntityListProps> = ({ title, initialItems }) => {
  const [items, setItems] = useState<Item[]>(initialItems);
  const [newItemValue, setNewItemValue] = useState<string>('');
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [expandedItemId, setExpandedItemId] = useState<number | null>(null);

  const toggleDropdown = () => {
    setIsOpen(prev => !prev);
  };

  const addItem = () => {
    if (newItemValue.trim()) {
      const newItem: Item = {
        id: items.length + 1,
        value: newItemValue,
      };
      setItems(prev => [...prev, newItem]);
      setNewItemValue('');
    }
  };

  const toggleItemDetails = (id: number) => {
    setExpandedItemId(prev => (prev === id ? null : id));
  };

  return (
    <div className='list-container'>
      <label className='label-show'>{title}</label>
      <button className='button-show' onClick={toggleDropdown}>
        {isOpen ? 'Скрыть' : 'Показать'}
      </button>
      {isOpen && (
        <div>
          <ul className='list'>
            {items.map(item => (
              <li className='item-list' key={item.id}>
                {item.value}
                <label>Связь</label>
                <button className='to-item-button' onClick={() => toggleItemDetails(item.id)}>
                  <img src='/home/denis/repository/SaigaWAF/assets/link.png' alt='' />
                </button>
              </li>
            ))}
          </ul>
          {/* <input 
            type="text" 
            value={newItemValue} 
            onChange={(e) => setNewItemValue(e.target.value)} 
            placeholder="Введите новое значение" 
          />
          <button className='add-item' onClick={addItem}>Добавить</button> */}
        </div>
      )}
    </div>
  );
};


