'use client';

import { useState, useEffect } from 'react';
import { API_BASE_URL } from '@/lib/api';

interface Channel {
  id: number;
  name: string;
}

interface Model {
  id: number;
  name: string;
  model_identifier: string;
  channel_id: number;
  channel?: Channel;
  display_name?: string | null;
  context_window?: number | null;
  max_tokens?: number | null;
  supports_tools?: boolean;
  supports_vision?: boolean;
  cost_input?: number | null;
  cost_output?: number | null;
  is_active: boolean;
  created_at: string;
}

export default function ModelsPage() {
  const [models, setModels] = useState<Model[]>([]);
  const [channels, setChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showImport, setShowImport] = useState(false);
  const [editingModel, setEditingModel] = useState<Model | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    model_identifier: '',
    channel_id: 0,
    is_active: true
  });

  useEffect(() => {
    fetchModels();
    fetchChannels();
  }, []);

  const fetchModels = async () => {
    try {
      const res = await fetch('${API_BASE_URL}/api/models/');
      const data = await res.json();
      setModels(data);
    } catch (error) {
      console.error('Failed to fetch models:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchChannels = async () => {
    try {
      const res = await fetch('${API_BASE_URL}/api/channels/');
      const data = await res.json();
      setChannels(data);
    } catch (error) {
      console.error('Failed to fetch channels:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const url = editingModel 
        ? `${API_BASE_URL}/api/models/${editingModel.id}/`
        : '${API_BASE_URL}/api/models/';
      const method = editingModel ? 'PUT' : 'POST';
      
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (res.ok) {
        await fetchModels();
        resetForm();
        alert('保存成功！');
      } else {
        const error = await res.json();
        alert(`保存失败: ${error.detail || '未知错误'}`);
      }
    } catch (error) {
      console.error('Failed to save model:', error);
      alert('保存失败，请检查网络连接');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('确定要删除这个模型吗？')) return;
    
    try {
      const res = await fetch(`${API_BASE_URL}/api/models/${id}/`, {
        method: 'DELETE'
      });
      if (res.ok) {
        fetchModels();
      }
    } catch (error) {
      console.error('Failed to delete model:', error);
    }
  };

  const handleEdit = (model: Model) => {
    setEditingModel(model);
    setFormData({
      name: model.name,
      model_identifier: model.model_identifier,
      channel_id: model.channel_id,
      is_active: model.is_active
    });
    setShowForm(true);
  };

  const handleImport = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formElement = e.currentTarget;
    const fileInput = formElement.querySelector('input[type="file"]') as HTMLInputElement;
    const file = fileInput?.files?.[0];
    
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('${API_BASE_URL}/api/models/import/', {
        method: 'POST',
        body: formData
      });

      if (res.ok) {
        fetchModels();
        setShowImport(false);
        alert('导入成功！');
      } else {
        const error = await res.json();
        alert(`导入失败: ${error.detail}`);
      }
    } catch (error) {
      console.error('Failed to import models:', error);
      alert('导入失败');
    }
  };

  const resetForm = () => {
    setFormData({ name: '', model_identifier: '', channel_id: 0, is_active: true });
    setEditingModel(null);
    setShowForm(false);
  };

  if (loading) {
    return <div className="px-4 py-6">加载中...</div>;
  }

  return (
    <div className="px-4 py-6">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">模型管理</h1>
          <p className="mt-2 text-sm text-gray-700">管理 AI 模型配置</p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none flex gap-2">
          <button
            onClick={() => setShowImport(!showImport)}
            className="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            {showImport ? '取消导入' : 'CSV 导入'}
          </button>
          <button
            onClick={() => setShowForm(!showForm)}
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700"
          >
            {showForm ? '取消' : '添加模型'}
          </button>
        </div>
      </div>

      {showImport && (
        <div className="mt-6 bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">CSV 批量导入</h2>
          <p className="text-sm text-gray-600 mb-4">
            CSV 格式：name,model_identifier,channel_id,is_active
          </p>
          <form onSubmit={handleImport} className="space-y-4">
            <div>
              <input
                type="file"
                accept=".csv"
                required
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700"
              >
                导入
              </button>
              <button
                type="button"
                onClick={() => setShowImport(false)}
                className="inline-flex justify-center rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
              >
                取消
              </button>
            </div>
          </form>
        </div>
      )}

      {showForm && (
        <div className="mt-6 bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">
            {editingModel ? '编辑模型' : '添加新模型'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">模型名称</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">模型标识符</label>
              <input
                type="text"
                required
                value={formData.model_identifier}
                onChange={(e) => setFormData({ ...formData, model_identifier: e.target.value })}
                placeholder="例如: gpt-4, claude-3-opus"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">所属渠道</label>
              <select
                required
                value={formData.channel_id}
                onChange={(e) => setFormData({ ...formData, channel_id: parseInt(e.target.value) })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              >
                <option value={0}>请选择渠道</option>
                {channels.map((channel) => (
                  <option key={channel.id} value={channel.id}>
                    {channel.name}
                  </option>
                ))}
              </select>
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
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">模型名称</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">标识符</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">所属渠道</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">状态</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">创建时间</th>
                    <th className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">操作</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {models.map((model) => (
                    <tr key={model.id}>
                      <td className="whitespace-nowrap px-3 py-4 text-sm font-medium text-gray-900">
                        {model.name}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {model.model_identifier}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {model.channel?.name || `渠道 ${model.channel_id}`}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                          model.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          {model.is_active ? '启用' : '禁用'}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {new Date(model.created_at).toLocaleString('zh-CN')}
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                        <button
                          onClick={() => handleEdit(model)}
                          className="text-indigo-600 hover:text-indigo-900 mr-4"
                        >
                          编辑
                        </button>
                        <button
                          onClick={() => handleDelete(model.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          删除
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {models.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                  暂无模型，点击"添加模型"或"CSV 导入"开始配置
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
