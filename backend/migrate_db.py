"""
数据库迁移脚本
从 SQLite 迁移到 PostgreSQL
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, Channel, Model, TestResult, ModelRanking


def migrate_database(source_url: str, target_url: str):
    """
    迁移数据库
    
    Args:
        source_url: 源数据库 URL (SQLite)
        target_url: 目标数据库 URL (PostgreSQL)
    """
    print(f"🔄 开始数据库迁移...")
    print(f"源: {source_url}")
    print(f"目标: {target_url}")
    
    # 连接源数据库
    source_engine = create_engine(source_url)
    SourceSession = sessionmaker(bind=source_engine)
    source_session = SourceSession()
    
    # 连接目标数据库
    target_engine = create_engine(target_url)
    TargetSession = sessionmaker(bind=target_engine)
    target_session = TargetSession()
    
    # 创建目标数据库表
    print("📝 创建目标数据库表...")
    Base.metadata.create_all(bind=target_engine)
    
    try:
        # 迁移渠道
        print("📦 迁移渠道数据...")
        channels = source_session.query(Channel).all()
        for channel in channels:
            target_session.merge(channel)
        target_session.commit()
        print(f"✅ 迁移了 {len(channels)} 个渠道")
        
        # 迁移模型
        print("📦 迁移模型数据...")
        models = source_session.query(Model).all()
        for model in models:
            target_session.merge(model)
        target_session.commit()
        print(f"✅ 迁移了 {len(models)} 个模型")
        
        # 迁移测试结果
        print("📦 迁移测试结果...")
        test_results = source_session.query(TestResult).all()
        for result in test_results:
            target_session.merge(result)
        target_session.commit()
        print(f"✅ 迁移了 {len(test_results)} 条测试结果")
        
        # 迁移排名
        print("📦 迁移模型排名...")
        rankings = source_session.query(ModelRanking).all()
        for ranking in rankings:
            target_session.merge(ranking)
        target_session.commit()
        print(f"✅ 迁移了 {len(rankings)} 条排名记录")
        
        print("🎉 数据库迁移完成！")
        
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        target_session.rollback()
        raise
    
    finally:
        source_session.close()
        target_session.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python migrate_db.py <source_url> <target_url>")
        print("示例: python migrate_db.py sqlite:///./aiswitch.db postgresql://user:pass@localhost/aiswitch")
        sys.exit(1)
    
    source_url = sys.argv[1]
    target_url = sys.argv[2]
    
    migrate_database(source_url, target_url)
