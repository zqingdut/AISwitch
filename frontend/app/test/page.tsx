'use client';

import { useState, useEffect } from 'react';
import { API_BASE_URL } from '@/lib/api';

interface Model {
  id: number;
  name: string;
  model_identifier: string;
}

interface TestResult {
  model_id: number;
  model_name: string;
  test_type: string;
  success: boolean;
  response_time: number;
  error_message?: string;
  created_at: string;
}

export default function TestPage() {
  const [models, setModels] = useState<Model[]>([]);
  const [selectedModels, setSelectedModels] = useState<number[]>([]);
  const [testType, setTestType] = useState('speed');
  const [testing, setTesting] = useState(false);
  const [results, setResults] = useState<TestResult[]>([]);

  useEffect(() => {
    fetchModels();
    fetchResults();
  }, []);

  const fetchModels = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/models/`);
      const data = await res.json();
      setModels(data.filter((m: Model & { is_active: boolean }) => m.is_active));
    } catch (error) {
      console.error('Failed to fetch models:', error);
    }
  };

  const fetchResults = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/test/results?limit=50`);
      const data = await res.json();
      setResults(data);
    } catch (error) {
      console.error('Failed to fetch results:', error);
    }
  };

  const handleTest = async () => {
    if (selectedModels.length === 0) {
      alert('请至少选择一个模型');
      return;
    }

    setTesting(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/test/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model_ids: selectedModels,
          test_type: testType
        })
      });

      if (res.ok) {
        alert('测试已启动，请稍后查看结果');
        fetchResults();
      } else {
        const error = await res.json();
        alert(`测试失败: ${error.detail}`);
      }
    } catch (error) {
      console.error('Failed to run test:', error);
      alert('测试失败');
    } finally {
      setTesting(false);
    }
  };

  const toggleModel = (modelId: number) => {
    setSelectedModels(prev => 
      prev.includes(modelId) 
        ? prev.filter(id => id !== modelId)
        : [...prev, modelId]
    );
  };

  const selectAll = () => {
    setSelectedModels(models.map(m => m.id));
  };

  const clearSelection = () => {
    setSelectedModels([]);
  };

  return (
    <div className="px-4 py-6">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">模型测试</h1>
        <p className="mt-2 text-sm text-gray-700">测试模型性能和质量</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 测试配置 */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">测试配置</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">测试类型</label>
              <select
                value={testType}
                onChange={(e) => setTestType(e.target.value)}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              >
                <option value="speed">速度测试</option>
                <option value="code">代码生成测试</option>
                <option value="tool">工具调用测试</option>
              </select>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium text-gray-700">选择模型</label>
                <div className="space-x-2">
                  <button
                    onClick={selectAll}
                    className="text-xs text-indigo-600 hover:text-indigo-900"
                  >
                    全选
                  </button>
                  <button
                    onClick={clearSelection}
                    className="text-xs text-gray-600 hover:text-gray-900"
                  >
                    清空
                  </button>
                </div>
              </div>
              <div className="border rounded-md p-3 max-h-64 overflow-y-auto">
                {models.length === 0 ? (
                  <p className="text-sm text-gray-500">暂无可用模型</p>
                ) : (
                  <div className="space-y-2">
                    {models.map((model) => (
                      <label key={model.id} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={selectedModels.includes(model.id)}
                          onChange={() => toggleModel(model.id)}
                          className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                        />
                        <span className="ml-2 text-sm text-gray-900">
                          {model.name} ({model.model_identifier})
                        </span>
                      </label>
                    ))}
                  </div>
                )}
              </div>
              <p className="mt-2 text-xs text-gray-500">
                已选择 {selectedModels.length} 个模型
              </p>
            </div>

            <button
              onClick={handleTest}
              disabled={testing || selectedModels.length === 0}
              className="w-full inline-flex justify-center items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {testing ? '测试中...' : '开始测试'}
            </button>
          </div>
        </div>

        {/* 测试说明 */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">测试说明</h2>
          <div className="space-y-4 text-sm text-gray-600">
            <div>
              <h3 className="font-medium text-gray-900 mb-1">速度测试</h3>
              <p>测试模型的响应速度，发送简单提示词并记录响应时间</p>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-1">代码生成测试</h3>
              <p>测试模型生成代码的能力，评估代码质量和准确性</p>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-1">工具调用测试</h3>
              <p>测试模型的函数调用能力，验证工具使用的准确性</p>
            </div>
          </div>
        </div>
      </div>

      {/* 测试结果 */}
      <div className="mt-8 bg-white shadow rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-medium text-gray-900">测试结果</h2>
          <button
            onClick={fetchResults}
            className="text-sm text-indigo-600 hover:text-indigo-900"
          >
            刷新
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">模型</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">测试类型</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">结果</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">响应时间</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">测试时间</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {results.map((result, idx) => (
                <tr key={idx}>
                  <td className="whitespace-nowrap px-3 py-4 text-sm font-medium text-gray-900">
                    {result.model_name}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {result.test_type === 'speed' && '速度测试'}
                    {result.test_type === 'code' && '代码生成'}
                    {result.test_type === 'tool' && '工具调用'}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm">
                    <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                      result.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {result.success ? '成功' : '失败'}
                    </span>
                    {result.error_message && (
                      <p className="text-xs text-red-600 mt-1">{result.error_message}</p>
                    )}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {result.response_time ? `${result.response_time.toFixed(2)}s` : '-'}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {new Date(result.created_at).toLocaleString('zh-CN')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {results.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              暂无测试结果
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
