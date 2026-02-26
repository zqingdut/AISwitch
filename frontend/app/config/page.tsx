'use client';

import { useState, useEffect } from 'react';

interface ModelRanking {
  id: number;
  name: string;
  model_identifier: string;
  rank: number;
  score: number;
  channel: {
    name: string;
    base_url: string;
  };
}

export default function ConfigPage() {
  const [rankings, setRankings] = useState<ModelRanking[]>([]);
  const [config, setConfig] = useState('');
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchRankings();
  }, []);

  const fetchRankings = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/models/ranking');
      const data = await res.json();
      setRankings(data);
    } catch (error) {
      console.error('Failed to fetch rankings:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateConfig = async () => {
    setGenerating(true);
    try {
      const res = await fetch('http://localhost:8000/api/config/generate', {
        method: 'POST'
      });
      const data = await res.json();
      setConfig(data.config);
    } catch (error) {
      console.error('Failed to generate config:', error);
      alert('生成配置失败');
    } finally {
      setGenerating(false);
    }
  };

  const downloadConfig = () => {
    const blob = new Blob([config], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'openclaw-config.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const copyConfig = () => {
    navigator.clipboard.writeText(config);
    alert('配置已复制到剪贴板');
  };

  if (loading) {
    return <div className="px-4 py-6">加载中...</div>;
  }

  return (
    <div className="px-4 py-6">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">配置生成</h1>
        <p className="mt-2 text-sm text-gray-700">生成 OpenClaw 配置文件</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 模型排名 */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-gray-900">模型排名</h2>
            <button
              onClick={fetchRankings}
              className="text-sm text-indigo-600 hover:text-indigo-900"
            >
              刷新
            </button>
          </div>

          {rankings.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>暂无排名数据</p>
              <p className="text-sm mt-2">请先进行模型测试以生成排名</p>
            </div>
          ) : (
            <div className="space-y-3">
              {rankings.map((model, index) => (
                <div
                  key={model.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                      index === 0 ? 'bg-yellow-100 text-yellow-800' :
                      index === 1 ? 'bg-gray-100 text-gray-800' :
                      index === 2 ? 'bg-orange-100 text-orange-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {index + 1}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{model.name}</p>
                      <p className="text-xs text-gray-500">{model.model_identifier}</p>
                      <p className="text-xs text-gray-400">{model.channel.name}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-gray-900">
                      {model.score ? model.score.toFixed(2) : '-'}
                    </p>
                    <p className="text-xs text-gray-500">分数</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          <button
            onClick={generateConfig}
            disabled={generating || rankings.length === 0}
            className="mt-6 w-full inline-flex justify-center items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {generating ? '生成中...' : '生成配置'}
          </button>
        </div>

        {/* 配置预览 */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-gray-900">配置预览</h2>
            {config && (
              <div className="space-x-2">
                <button
                  onClick={copyConfig}
                  className="text-sm text-indigo-600 hover:text-indigo-900"
                >
                  复制
                </button>
                <button
                  onClick={downloadConfig}
                  className="text-sm text-indigo-600 hover:text-indigo-900"
                >
                  下载
                </button>
              </div>
            )}
          </div>

          {!config ? (
            <div className="text-center py-8 text-gray-500">
              <p>点击"生成配置"按钮生成 OpenClaw 配置</p>
            </div>
          ) : (
            <div className="relative">
              <pre className="bg-gray-50 rounded-lg p-4 text-xs overflow-x-auto max-h-96 overflow-y-auto">
                <code>{config}</code>
              </pre>
            </div>
          )}
        </div>
      </div>

      {/* 使用说明 */}
      <div className="mt-8 bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">使用说明</h2>
        <div className="space-y-3 text-sm text-gray-600">
          <div className="flex items-start">
            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xs font-bold mr-3">1</span>
            <p>确保已完成模型测试，系统会根据测试结果生成排名</p>
          </div>
          <div className="flex items-start">
            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xs font-bold mr-3">2</span>
            <p>点击"生成配置"按钮，系统会根据排名自动生成 OpenClaw 配置</p>
          </div>
          <div className="flex items-start">
            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xs font-bold mr-3">3</span>
            <p>复制或下载配置文件，将其应用到 OpenClaw 中</p>
          </div>
          <div className="flex items-start">
            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xs font-bold mr-3">4</span>
            <p>配置会按照性能排名自动选择最优模型进行切换</p>
          </div>
        </div>
      </div>
    </div>
  );
}
