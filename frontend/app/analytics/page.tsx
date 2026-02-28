'use client';

import { useState, useEffect } from 'react';
import { API_BASE_URL } from '@/lib/api';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface TestHistory {
  date: string;
  test_type: string;
  total: number;
  success_count: number;
  success_rate: number;
  avg_response_time: number | null;
}

interface ModelComparison {
  model_id: number;
  model_name: string;
  total_tests: number;
  success_count: number;
  success_rate: number;
  avg_response_time: number | null;
  avg_quality: number | null;
}

interface TestTypeDistribution {
  test_type: string;
  count: number;
  success_count: number;
  success_rate: number;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function AnalyticsPage() {
  const [days, setDays] = useState(7);
  const [testHistory, setTestHistory] = useState<TestHistory[]>([]);
  const [modelComparison, setModelComparison] = useState<ModelComparison[]>([]);
  const [testDistribution, setTestDistribution] = useState<TestTypeDistribution[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, [days]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const [historyRes, comparisonRes, distributionRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/analytics/test-history?days=${days}`),
        fetch(`${API_BASE_URL}/api/analytics/model-comparison?days=${days}`),
        fetch(`${API_BASE_URL}/api/analytics/test-type-distribution?days=${days}`)
      ]);

      const [historyData, comparisonData, distributionData] = await Promise.all([
        historyRes.json(),
        comparisonRes.json(),
        distributionRes.json()
      ]);

      setTestHistory(historyData);
      setModelComparison(comparisonData);
      setTestDistribution(distributionData);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  // 按日期聚合数据用于趋势图
  const aggregateByDate = () => {
    const dateMap = new Map<string, any>();
    
    testHistory.forEach(item => {
      if (!dateMap.has(item.date)) {
        dateMap.set(item.date, {
          date: item.date,
          total: 0,
          success: 0,
          avgResponseTime: 0,
          count: 0
        });
      }
      
      const entry = dateMap.get(item.date);
      entry.total += item.total;
      entry.success += item.success_count;
      if (item.avg_response_time) {
        entry.avgResponseTime += item.avg_response_time;
        entry.count += 1;
      }
    });

    return Array.from(dateMap.values()).map(item => ({
      date: item.date,
      total: item.total,
      successRate: item.total > 0 ? (item.success / item.total * 100).toFixed(1) : 0,
      avgResponseTime: item.count > 0 ? (item.avgResponseTime / item.count).toFixed(0) : 0
    }));
  };

  const trendData = aggregateByDate();

  if (loading) {
    return <div className="px-4 py-6">加载中...</div>;
  }

  return (
    <div className="px-4 py-6">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">数据分析</h1>
          <p className="mt-2 text-sm text-gray-700">测试历史数据可视化</p>
        </div>
        
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-700">时间范围：</label>
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
          >
            <option value={7}>最近 7 天</option>
            <option value={14}>最近 14 天</option>
            <option value={30}>最近 30 天</option>
          </select>
        </div>
      </div>

      {/* 测试趋势 */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">测试趋势</h2>
        {trendData.length === 0 ? (
          <div className="text-center py-12 text-gray-500">暂无数据</div>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="successRate"
                stroke="#10b981"
                name="成功率 (%)"
                strokeWidth={2}
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="avgResponseTime"
                stroke="#3b82f6"
                name="平均响应时间 (ms)"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* 模型对比 */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">模型性能对比</h2>
          {modelComparison.length === 0 ? (
            <div className="text-center py-12 text-gray-500">暂无数据</div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={modelComparison}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="model_name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="success_rate" fill="#10b981" name="成功率 (%)" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* 测试类型分布 */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">测试类型分布</h2>
          {testDistribution.length === 0 ? (
            <div className="text-center py-12 text-gray-500">暂无数据</div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={testDistribution}
                  dataKey="count"
                  nameKey="test_type"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={(props) => {
                    const payload = (props as any).payload as any;
                    return payload?.test_type && payload?.count != null
                      ? `${payload.test_type}: ${payload.count}`
                      : undefined;
                  }}
                >
                  {testDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* 模型详细统计 */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">模型详细统计</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">模型</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">测试次数</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">成功率</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">平均响应时间</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">平均质量分</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {modelComparison.map((model) => (
                <tr key={model.model_id}>
                  <td className="whitespace-nowrap px-3 py-4 text-sm font-medium text-gray-900">
                    {model.model_name}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {model.total_tests}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm">
                    <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                      model.success_rate >= 80 ? 'bg-green-100 text-green-800' :
                      model.success_rate >= 50 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {model.success_rate.toFixed(1)}%
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {model.avg_response_time ? `${model.avg_response_time.toFixed(0)} ms` : '-'}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {model.avg_quality ? model.avg_quality.toFixed(2) : '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {modelComparison.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              暂无数据
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
