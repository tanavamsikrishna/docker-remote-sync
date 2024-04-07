function run
    switch "$argv[1]"
        case release
            set git_status (git status --porcelain)
            set -q git_status[1]; and begin
                echo "Untracked/uncommited files exist"
                return 1
            end
            read -f -P "New tag (a.b.c): " tag; or return
            sd '^version = ".*"' 'version = "'$tag'"' pyproject.toml; or return
            git add .
            git commit -m "Bump up version to "$tag
            git push
            git tag $tag
            git push --tags
            gh release create v$tag
    end
end
