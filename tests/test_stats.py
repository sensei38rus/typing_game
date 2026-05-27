from src.stats import Stats

def test_stats_accuracy_calculation(tmp_path):
    stats_file = tmp_path / "progress.json"
    stats = Stats(data_file=str(stats_file))
    
    
    assert stats.get_accuracy() == 100.0
    
    
    stats.record_success("hello")
    stats.record_fail("world")
    
    
    assert stats.get_accuracy() == 50.0

def test_stats_saving_and_loading(tmp_path):
    stats_file = tmp_path / "progress.json"
    
    
    stats1 = Stats(data_file=str(stats_file))
    stats1.record_success("test")
    stats1.save_final_score(1500)
    
    
    stats2 = Stats(data_file=str(stats_file))
    
    assert stats2.final_score == 1500
    assert len(stats2.successes) == 1
    assert stats2.successes[0]["word"] == "test"