'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Channel {
  id: number;
  name: string;
  base_url: string;
  api_key: string;
  auth_type?: string;
  headers?: any;
  is_active: boolean;
  created_at: string;
  updated_at?: string | null;
}

export default function ChannelsPage() {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingChannel, setEditingChannel] = useState<Channel | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    base_url: '',
    api_key: '',
    is_active: true
  });

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/channels/');
      const data = await res.json();
      setChannels(data);
    } catch (error) {
      console.error('Failed to fetch channels:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const url = editingChannel 
        ? `http://localhost:8000/api/channels/${editingChannel.id}/`
        : 'http://localhost:8000/api/channels/';
      const method = editingChannel ? 'PUT' : 'POST';
      
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (res.ok) {
        await fetchChannels();
        resetForm();
        alert('保存成功！');
      } else {
        const error = await res.json();
        alert(`保存失败: ${error.detail || '未知错误'}`);
      }
    } catch (error) {
      console.error('Failed to save channel:', error);
      alert('保存失败，请检查网络连接');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('确定要删除这个渠道吗？')) return;
    
    try {
      const res = await fetch(`http://localhost:8000/api/channels/${id}/`, {
        method: 'DELETE'
      });
      if (res.ok) {
        fetchChannels();
      }
    } catch (error) {
      console.error('Failed to delete channel:', error);
    }
  };

  const handleEdit = (channel: Channel) => {
    setEditingChannel(channel);
    setFormData({
      name: channel.name,
      base_url: channel.base_url,
      api_key: channel.api_key,
      is_active: channel.is_active
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({ name: '', base_url: '', api_key: '', is_active: true });
    setEditingChannel(null);
    setShowForm(false);
  };

  if (loading) {
    return <div className="px-4 py-6">加载中...</div>;
  }

  return (
    <div className="px-4 py-6">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">渠道管理</h1>
          <p className="mt-2 text-sm text-gray-700">管理 API 渠道配置</p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            onClick={() => setShowForm(!showForm)}
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700"
          >
            {showForm ? '取消' : '添加渠道'}
          </button>
        </div>
      </div>

      {showForm && (
        <div className="mt-6 bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">
            {editingChannel ? '编辑渠道' : '添加新渠道'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">名称</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Base URL</label>
              <input
                type="url"
                required
                value={formData.base_url}
                onChange={(e) => setFormData({ ...formData, base_url: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">API Key</label>
              <input
                type="password"
                required
                value={formData.api_key}
                onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <label className="ml-2 block text-sm text-gray-900">启用</label>
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700"
              >
                保存
              </button>
              <button
                type="button"
                onClick={resetForm}
                className="inline-flex justify-center rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
              >
                取消
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="mt-8 flex flex-col">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table className="min-w-full divide-y divide-gray-300">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">名称</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Base URL</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">状态</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">创建时间</th>
                    <th className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">操作</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {channels.map((channel) => (
                    <tr key={channel.id}>
                      <td className="whitespace-nowrap px-3 py-4 text-sm font-medium text-gray-900">
                        {channel.name}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {channel.base_url}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                          channel.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          {channel.is_active ? '启用' : '禁用'}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {new Date(channel.created_at).toLocaleString('zh-CN')}
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                        <button
                          onClick={() => handleEdit(channel)}
                          className="text-indigo-600 hover:text-indigo-900 mr-4"
                        >
                          编辑
                        </button>
                        <button
                          onClick={() => handleDelete(channel.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          删除
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {channels.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                  暂无渠道，点击"添加渠道"开始配置
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
