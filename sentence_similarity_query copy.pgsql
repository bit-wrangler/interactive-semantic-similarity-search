with ref_sentences as (
	select 
		s1.id, 
		s1.embedding,
        phraseto_tsquery('english', s1.text) as text_query
	from sentences s1
	where s1.document_id = 1
), t1 as (
	select
		*
	from ref_sentences r,
	lateral (
		select 
			s.document_id as potential_match_id,
			MAX((s.embedding <#> r.embedding) * -1) * 1 AS score,
            0 AS text_score
		from sentences s
		where s.document_id != 1 and ((s.embedding <#> r.embedding) * -1) > 0.45
		group by s.document_id
	) ss
)
select
	t1.potential_match_id as result_id,
	SUM(t1.score + t1.text_score) as doc_score
from t1
group by t1.potential_match_id
order by doc_score desc
limit 50